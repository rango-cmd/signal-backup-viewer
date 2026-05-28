import os
import zipfile

def build_zip_file_cache(zip_path, target_dir):
    file_cache = {}
    with zipfile.ZipFile(zip_path, 'r') as z:
        # 尋找 ZIP 內部的 main.jsonl 所在位置，藉此推算真正的內層根目錄
        jsonl_internal_path = next((name for name in z.namelist() if name.endswith('main.jsonl')), None)
        if not jsonl_internal_path:
            return file_cache
            
        zip_root = os.path.dirname(jsonl_internal_path)

        for info in z.infolist():
            if info.is_dir() or info.filename.endswith('main.jsonl'):
                continue
            
            f_size = info.file_size
            _, f_ext = os.path.splitext(info.filename)
            f_ext = f_ext.lower()
            
            # 去除 ZIP 包裹的雙層目錄前綴，取得乾淨的相對路徑 (例如 files/00/xxx.jpg)
            clean_rel_path = os.path.relpath(info.filename, zip_root)
            
            out_path = os.path.join(target_dir, clean_rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            with z.open(info.filename) as source, open(out_path, 'wb') as target:
                target.write(source.read())
            
            file_cache[(f_size, f_ext)] = clean_rel_path
    return file_cache