# run.py
import os
from src.cache import build_disk_file_cache
from src.parser import parse_signal_backup, get_tz_str
from src.renderer import generate_html_output

JSONL_FILE = 'main.jsonl'
OUTPUT_HTML = 'messages.html'

def main():
    print("=" * 50)
    print(" Signal Backup to Telegram-Style HTML Converter ")
    print("=" * 50)
    
    # 1. 獲取時區後綴
    tz_suffix = get_tz_str()
    
    # 2. 自動偵測媒體資料夾並建立大小快取
    base_dir = './files' if os.path.exists('./files') else 'attachments.noindex'
    disk_cache = build_disk_file_cache(base_dir)
    
    # 3. 解析 main.jsonl 核心原廠欄位
    if not os.path.exists(JSONL_FILE):
        print(f"❌ 錯誤：找不到核心備份檔 '{JSONL_FILE}'，請將它放在專案根目錄下。")
        return
        
    recipients, chat_to_recipient, chats, chat_meta, self_real_name = parse_signal_backup(JSONL_FILE)
    
    # 4. 渲染 100% 複製的 Telegram 官方雙欄嵌套網頁
    full_html = generate_html_output(recipients, chat_to_recipient, chats, chat_meta, self_real_name, disk_cache, tz_suffix)
    
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print("\n🎉 [轉換完成] 完美版網頁已成功生成！")
    print(f"👉 請在瀏覽器中直接雙擊打開：'{OUTPUT_HTML}'")
    print("=" * 50)

if __name__ == "__main__":
    main()