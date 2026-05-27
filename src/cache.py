# src/cache.py
import os

def build_disk_file_cache(base_dir):

    file_cache = {}

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            full_path = os.path.join(root, f)
            
            # 取得檔案大小
            f_size = os.path.getsize(full_path)
            
            # 取得副檔名並強制轉為小寫
            _, f_ext = os.path.splitext(f)
            f_ext = f_ext.lower()
                
            # 使用 (大小, 副檔名) 作為複合鍵
            composite_key = (f_size, f_ext)
            file_cache[composite_key] = full_path
            
    return file_cache