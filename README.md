# Menu Translator (Prototype)

AIを使ったメニュー翻訳アプリのプロトタイプです。  
写真に写したメニューから文字を抽出し、直訳ではなく「観光客にわかりやすい自然な料理名＋説明」を生成AIで翻訳します。  

---

## 🚀 機能 (MVP段階)
- 画像からOCRで文字を抽出（日本語・英語・中国語・韓国語対応）
- OpenAI APIを使った自然な翻訳
- 多言語出力（英語・中国語・韓国語）
- CLI実行で結果を確認
-  「からあげ」を英訳した際に「Karaage」ではなく、「Fried chicken」と翻訳されるようにする
---

## 📦 セットアップ手順

### 1. 初期セットアップ
1. SourceTreeにてクローン
```bash
git@github.com:TakumiKusuyama/global-menu-translator.git
```

2. .giignoreを作成してコミット。初期ブッシュ
