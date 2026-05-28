import os
import argparse
from src.cache import build_zip_file_cache
from src.parser import parse_signal_backup_from_zip, get_tz_str
from src.renderer import generate_html_output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.file):
        return

    base_name = os.path.splitext(os.path.basename(args.file))[0]
    target_dir = os.path.join(args.output, base_name)
    os.makedirs(target_dir, exist_ok=True)

    tz_suffix = get_tz_str()
    disk_cache = build_zip_file_cache(args.file, target_dir)
    
    recipients, chat_to_recipient, chats, chat_meta, self_real_name = parse_signal_backup_from_zip(args.file)
    full_html = generate_html_output(recipients, chat_to_recipient, chats, chat_meta, self_real_name, disk_cache, tz_suffix)
    
    with open(os.path.join(target_dir, 'messages.html'), 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    main()