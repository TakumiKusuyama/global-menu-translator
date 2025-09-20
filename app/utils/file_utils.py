import tempfile
import os

"""アップロードファイルを一時保存し、パスを返す"""
def save_upload_file(upload_file, suffix=".jpg") -> str:    
    try:
        # プロジェクト配下のtmpディレクトリに保存
        tmp_dir = os.path.join(os.path.dirname(__file__), '../../tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(suffix=suffix, dir=tmp_dir)
        with os.fdopen(fd, 'wb') as tmp:
            tmp.write(upload_file.file.read())
        return os.path.abspath(tmp_path)
    except Exception as e:
        raise RuntimeError(f"ファイル保存に失敗しました: {e}")