import os
import zipfile

def build_zip_file_cache(zip_path, target_dir):
    file_cache = {}
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            
            f_size = info.file_size
            _, f_ext = os.path.splitext(info.filename)
            f_ext = f_ext.lower()
            
            # 建立記憶體映射，Value 改為儲存該檔案在 ZIP 內的原始路徑與輸出目標
            file_cache[(f_size, f_ext)] = {
                'zip_internal_path': info.filename,
                'target_dir': target_dir
            }
    return file_cache