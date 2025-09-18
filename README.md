## 機能概要
- 画像から日本語・英語・中国語・韓国語のテキストをOCR抽出
- OpenAI APIによる自然な料理名・説明への翻訳
- 多言語対応（翻訳先言語はAPIで指定可能）
- FastAPIによるWeb API（/translate_menu）

---

## ディレクトリ構成

```
global-menu-translator/
├── app/
│   ├── main.py                # FastAPIエントリポイント
│   ├── config.py             # 設定ファイル（定数管理）
│   ├── services/
│   │   ├── ocr_service.py
│   │   ├── language_service.py
│   │   └── translation_service.py
│   └── utils/
│       └── file_utils.py
├── requirements.txt
├── .env                      # APIキーや環境依存設定
├── README.md
└── test_env.py
```

---

## セットアップ手順


### 1. 仮想環境の作成とパッケージインストール

1. 仮想環境(venv)の作成
	```sh
	python3 -m venv venv
	```
2. 仮想環境の有効化（macOS/Linux）
	```sh
	source venv/bin/activate
	```
3. パッケージのインストール
	```sh
	pip install -r requirements.txt
	```

※ 仮想環境を有効化した状態（プロンプトに (venv) が表示される）で開発・実行してください。

### 2. .envファイルの作成・編集

ルート直下に `.env` を作成し、下記のようにAPIキーやモデル名を記載してください。

```
TRANSLATION_API_KEY=sk-xxxx...
MODEL_NAME_3.5_TURBO=gpt-3.5-turbo
INPUT_IMAGE_DIR=./input_images
OUTPUT_DIR=./output
```

### 3. Tesseract OCRのインストール（macOSの場合）

```sh
brew install tesseract
brew install tesseract-lang
```

### 4. サーバーの起動

```sh
uvicorn app.main:app --reload
```

### 5. APIの利用

ブラウザで http://localhost:8000/docs にアクセスし、Swagger UIから `/translate_menu` エンドポイントをテストできます。

---

## 必要パッケージ一覧（requirements.txt例）

```
fastapi
uvicorn
openai
python-dotenv
pytesseract
Pillow
pytest
```

---

## 補足
- WindowsやLinuxの場合はTesseractのインストール方法が異なります。
- .envのAPIキーやパスは環境ごとに変更してください。
- 詳細な実装や拡張は app/ 配下の各サービスをご参照ください。


---

## 🧪 自動テスト（おすすめ）

FastAPIのTestClient＋pytestを使うと、簡単にAPIの自動テストができます。

### 1. テストファイル例（tests/test_api.py）
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_translate_menu():
	# ダミー画像ファイルを用意（例: sample.jpg）
	with open("sample.jpg", "rb") as img:
		response = client.post(
			"/translate_menu",
			files={"file": ("sample.jpg", img, "image/jpeg")},
			data={"target_lang": "en"}
		)
	assert response.status_code == 200
	assert "translated_text" in response.json()
```

---

## 🧪 テストの実施方法

1. 仮想環境を有効化し、依存パッケージをインストール済みであることを確認してください。
2. テスト用画像（例: tests/data/sample.jpg）が存在することを確認してください。
3. プロジェクトルートで以下を実行します。

```sh
pytest
```

`tests/` 配下のテストが自動で実行されます。

### デバッグ実行
- ブレークポイントをソース内に追記
```python
breakpoint()
```
- コマンド実行
```sh
pytest -s
```

#### よく使うPDBコマンド
```
n（next）：次の行に進む
s（step）：関数の中に入る
c（continue）：次のブレークポイントまたは終了まで進める
l（list）：周辺のソースコードを表示
p 変数名：変数の値を表示（例：p OPENAI_API_KEY）
q：デバッグを終了して抜ける
```

# Global Menu Translator

AIを活用した多言語メニュー翻訳Webアプリです。画像からメニューをOCRで抽出し、OpenAI APIで観光客向けに自然な翻訳を行います。

---