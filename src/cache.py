import os
import zipfile

def build_zip_file_cache(zip_path, target_dir):
    file_cache = {}
    with zipfile.ZipFile(zip_path, 'r') as z:
        jsonl_path = next((name for name in z.namelist() if name.endswith('main.jsonl')), None)
        if not jsonl_path:
            return file_cache, None
            
        zip_root = os.path.dirname(jsonl_path)

        out_jsonl = os.path.join(target_dir, 'main.jsonl')
        with z.open(jsonl_path) as src, open(out_jsonl, 'wb') as tgt:
            tgt.write(src.read())

        for info in z.infolist():
            if info.is_dir() or info.filename.endswith('main.jsonl'):
                continue
            
            f_size = info.file_size
            f_ext = os.path.splitext(info.filename)[1].lower()
            clean_rel_path = os.path.relpath(info.filename, zip_root)
            out_path = os.path.join(target_dir, clean_rel_path)
            
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with z.open(info.filename) as src, open(out_path, 'wb') as tgt:
                tgt.write(src.read())
            
            file_cache[(f_size, f_ext)] = clean_rel_path
            
    return file_cache, jsonl_path