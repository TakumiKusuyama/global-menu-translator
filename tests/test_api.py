from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_translate_menu():
    # テスト用画像ファイルのパス
    img_path = "tests/data/sample.jpg"
    try:
        with open(img_path, "rb") as img:
            response = client.post(
                "/translate_menu",
                files={"file": ("sample.jpg", img, "image/jpeg")},
                data={"target_lang": "ja"}
            )
        assert response.status_code == 200
        assert "translated_text" in response.json()
    except FileNotFoundError:
        # テスト画像が無い場合はスキップ
        pass
