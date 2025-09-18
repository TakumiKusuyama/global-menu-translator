import tempfile

"""アップロードファイルを一時保存し、パスを返す"""
def save_upload_file(upload_file, suffix=".jpg") -> str:    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(upload_file.file.read())
            return tmp.name
    except Exception as e:
        raise RuntimeError(f"ファイル保存に失敗しました: {e}")