import os
import gradio as gr
from src.cache import build_zip_file_cache
from src.parser import parse_signal_backup_from_zip, get_tz_str
from src.renderer import generate_html_output

def convert_signal_backup(zip_file, output_base_dir):
    if not zip_file or not output_base_dir:
        return "❌ 錯誤：請確認是否已選擇輸入檔案與輸出目錄。"
        
    zip_path = zip_file.name
    base_name = os.path.splitext(os.path.basename(zip_path))[0]
    target_dir = os.path.join(output_base_dir, base_name)
    os.makedirs(target_dir, exist_ok=True)

    try:
        tz_suffix = get_tz_str()
        disk_cache, jsonl_internal_path = build_zip_file_cache(zip_path, target_dir)
        
        if not jsonl_internal_path:
            return "❌ 錯誤：壓縮檔中找不到核心備份資料 main.jsonl。"

        recipients, chat_to_recipient, chats, chat_meta, self_real_name = parse_signal_backup_from_zip(zip_path, jsonl_internal_path)
        full_html = generate_html_output(recipients, chat_to_recipient, chats, chat_meta, self_real_name, disk_cache, tz_suffix)
        
        with open(os.path.join(target_dir, 'messages.html'), 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        return f"🎉 轉換成功！\n📂 備份檔、原始 main.jsonl 與網頁已安全輸出至：\n{os.path.abspath(target_dir)}"
    except Exception as e:
        return f"❌ 轉換失敗，錯誤回報：{str(e)}"

with gr.Blocks(title="Signal Backup Viewer Converter") as demo:
    gr.Markdown("# 💬 Signal 備份資料轉換器 (Telegram 風格)")
    gr.Markdown("將 Signal 導出的加密 ZIP 壓縮包，一鍵轉換為具備雙欄導覽、左右氣泡分流的現代化網頁。")
    
    with gr.Row():
        with gr.Column():
            input_file = gr.File(label="1. 拖放或上傳 Signal 備份壓縮檔 (.zip)", file_types=[".zip"])
            output_dir = gr.Textbox(label="2. 輸入輸出主目錄路徑", value="./output")
            btn_start = gr.Button("🚀 開始轉換", variant="primary")
        with gr.Column():
            status_output = gr.Textbox(label="執行狀態與回報結果", interactive=False, lines=6)
            
    btn_start.click(fn=convert_signal_backup, inputs=[input_file, output_dir], outputs=status_output)

if __name__ == "__main__":
    demo.launch(inbrowser=True)