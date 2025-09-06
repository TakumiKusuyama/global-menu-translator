# Menu Translator (Prototype)

AIを使ったメニュー翻訳アプリのプロトタイプです。  
写真に写したメニューから文字を抽出し、直訳ではなく「観光客にわかりやすい自然な料理名＋説明」を生成AIで翻訳します。  

---

## 🚀 機能 (MVP段階)
- 画像からOCRで文字を抽出（日本語・英語・中国語・韓国語対応）
- OpenAI APIを使った自然な翻訳
- 多言語出力（英語・中国語・韓国語）
- 画像はアプリ内での撮影およびアップロードのみとする
-  「からあげ」を英訳した際に「Karaage」ではなく、「Fried chicken」と翻訳されるようにする
---
## 機能（MVP後）
- 写真撮影でAR機能でリアルタイム翻訳を可能とする
- 翻訳のみではなく、使用食材やアレルギー食材なども出力する

---

## 📦 セットアップ手順

### 1. 初期セットアップ
1. SourceTreeにてクローン
```bash
git@github.com:TakumiKusuyama/global-menu-translator.git
```

2. .giignoreを作成してコミット。初期ブッシュ

### 2. 必要ライブラリ
/global-menu-translator/requirements.txt に以下を追加
```txt
pytesseract
Pillow
openai
```

### 3. Python環境準備
- /global-menu-translatorにて以下コマンドを叩く
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- pipのバージョンが低い旨のWarningが出たら以下コマンドを叩く
```bash
python -m pip install --upgrade pip
```

### 4. Tesseract OCRのインストール (Mac)
```bash
brew install tesseract
brew install tesseract-lang
```

### 5. OpenAI APIキー設定

#### 1. 環境変数にAPIキーを設定
- ルートディレクトリに.envを作成し、下記を記述
```bash
OPENAI_API_KEY="my_api_key"
```
#### 2. APIが設定できたかの確認
- ルートにtest_env.pyを作成し、仮想環境下で実行
```bash
(venv) (3.10.4) tk@tknoMacBook-Pro global-menu-translator % python test_env.py
```
- 仮想環境下であるかの確認
    - (venv)が入っているか
    - 下記で/venv/bin/pythonになっているか
    ```bash
    which python
    ```
- 仮想環境ではない場合、下記を叩く
```bash
source venv/bin/activate
```
- dotenvが存在しないエラーが発生した場合
    - 仮想環境下で下記を叩き、インストール
    ```bash
    pip install python-dotenv
    ```
    - global-menu-translator/requirements.txtに下記を追加
    ```txt
    python-dotenv
    ```
- ルートで下記実行
```bash
python test_env.py
```

### 6. 