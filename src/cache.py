# src/cache.py
import os

def build_disk_file_cache(base_dir):
    """走訪所有子資料夾，建立 { 檔案大小_bytes: '實體路徑' } 的快取字典"""
    file_cache = {}
    print(f"📦 正在掃描媒體資料夾 '{base_dir}' 建立大小索引...")
    
    if not os.path.exists(base_dir):
        print(f"⚠️ 提示：未找到媒體資料夾 '{base_dir}'，圖片將顯示為預留文字。")
        return file_cache

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                f_size = os.path.getsize(full_path)
                file_cache[f_size] = full_path
            except:
                continue
                
    print(f"✅ 實體檔案索引建立完成，共搜集到 {len(file_cache)} 個媒體檔案。")
    return file_cache