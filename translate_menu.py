import os
import sys
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from langdetect import detect, DetectorFactory

# 言語コードと名称の対応表
LANG_CODE_TO_NAME = {
    "ja": "Japanese",
    "en": "English",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    # 必要に応じて追加
}

# .env 読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# OpenAI API キーの取得
if not openai_api_key:
    print("Error: OPENAI_API_KEY is not set in the environment variables.")
    sys.exit(1)
# OpenAI クライアント初期化
client = OpenAI(api_key=openai_api_key)

# OCRで利用する言語コード（必要に応じて拡張可能）
# Tesseract OCR 言語コードと LANG_CODE_TO_NAME の対応:
#   jpn     -> ja (Japanese)
#   eng     -> en (English)
#   chi_sim -> zh-cn (Chinese Simplified)
#   chi_tra -> zh-tw (Chinese Traditional)
OCR_LANG_CODES = "jpn+eng+chi_sim+chi_tra"

# 画像ファイル名（コマンドライン引数から取得）
image_path = sys.argv[1]

DetectorFactory.seed = 0  # 安定化のためのシード設定

# OCRで文字抽出
def extract_text(image_path: str, ocr_lang: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=ocr_lang)
    return text

# 言語自動判定
def detect_language(text: str) -> str:
    lang_code = detect(text)
    return lang_code

# 翻訳
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    prompt = f"""
    Translate the following menu text from {source_lang} to {target_lang}.
    Please provide natural, tourist-friendly menu names, not literal translations.

    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # コマンドライン引数: 1つ目=画像ファイル名, 2つ目=翻訳先言語コード
    if len(sys.argv) < 3:
        print("Usage: python translate_menu.py <image_path> <target_lang_code>")
        print("例: python translate_menu.py sample_menu.jpg en")
        sys.exit(1)
    extracted = extract_text(image_path, ocr_lang=OCR_LANG_CODES)
    print("📝 OCR抽出結果:\n", extracted)
    target_lang_code = sys.argv[2]

    # 言語自動判定
    detected_lang_code = detect_language(extracted)
    source_lang = LANG_CODE_TO_NAME.get(detected_lang_code, "Unknown")
    target_lang = LANG_CODE_TO_NAME.get(target_lang_code)

    if source_lang == "Unknown":
        print("対応していない言語です。")
        sys.exit(1)
    if target_lang is None:
        print(f"対応していない翻訳先言語コードです: {target_lang_code}")
        sys.exit(1)
    else:
        translated = translate_text(extracted, source_lang, target_lang)
        print("\n🌐 翻訳結果:\n", translated)
