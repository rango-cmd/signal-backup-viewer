import os
from src.cache import build_disk_file_cache
from src.parser import parse_signal_backup, get_tz_str
from src.renderer import generate_html_output

JSONL_FILE = 'main.jsonl'
OUTPUT_HTML = 'messages.html'

def main():
    tz_suffix = get_tz_str()
    base_dir = './files' if os.path.exists('./files') else 'attachments.noindex'
    disk_cache = build_disk_file_cache(base_dir)
    
    if not os.path.exists(JSONL_FILE):
        return
        
    recipients, chat_to_recipient, chats, chat_meta, self_real_name = parse_signal_backup(JSONL_FILE)
    full_html = generate_html_output(recipients, chat_to_recipient, chats, chat_meta, self_real_name, disk_cache, tz_suffix)
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    main()