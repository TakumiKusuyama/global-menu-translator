import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# .env 読み込み
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# OCRで文字抽出
def extract_text(image_path: str, ocr_lang: str = "jpn") -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=ocr_lang)
    return text

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
    # 例: 中国語のメニューを日本語に翻訳
    image_path = "sample_menu.jpg"
    source_lang = "Chinese"
    target_lang = "Japanese"
    ocr_lang = "chi_sim"  # OCR入力言語

    extracted = extract_text(image_path, ocr_lang=ocr_lang)
    print("📝 OCR抽出結果:\n", extracted)

    translated = translate_text(extracted, source_lang, target_lang)
    print("\n🌐 翻訳結果:\n", translated)
