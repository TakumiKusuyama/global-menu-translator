import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import OpenAI

from app.services.ocr_service import OCRService
from app.services.language_service import LanguageService
from app.services.translation_service import TranslationService
from app.utils.file_utils import save_upload_file
from app.config import DEFAULT_TARGET_LANG
from app.utils.image_draw import draw_translated_text_on_image

load_dotenv()
# APIキーは.envから取得（必要に応じて環境変数と組み合わせてもOK）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in .env")

# 各サービスの初期化
openai_client = OpenAI(api_key=OPENAI_API_KEY)
ocr_service = OCRService()
language_service = LanguageService(openai_client)
translation_service = TranslationService(openai_client)

# FastAPIアプリケーションの生成
app = FastAPI()

"""
画像ファイルを受け取り、OCR→言語判定→翻訳を行うAPIエンドポイント
"""
@app.post("/translate_menu")
async def translate_menu(
    file: UploadFile = File(...),
    target_lang: str = Form(DEFAULT_TARGET_LANG, description="Target language (e.g. English, Japanese, French)")
):
    # 1. 画像を一時保存
    try:
        temp_image_path = save_upload_file(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"画像保存エラー: {e}")

    # 2. OCR（前処理も含む）
    try:
        menu_text = ocr_service.extract_text(temp_image_path)
        # 各行のバウンディングボックスも取得
        text_boxes = ocr_service.extract_text_with_boxes(temp_image_path)
    except Exception as e:
        os.unlink(temp_image_path)
        raise HTTPException(status_code=500, detail=f"OCRエラー: {e}")
    finally:
        os.unlink(temp_image_path)

    if not menu_text.strip():
        raise HTTPException(status_code=400, detail="画像からテキストを検出できませんでした。")

    logging.info(f"[LOG] 原文: {menu_text}")

    # 3. 言語判定
    try:
        # detected_language = language_service.detect_language(menu_text)
        detected_language = language_service.detect_language(menu_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"言語判定エラー: {e}")
    logging.info(f"[LOG] 画像の言語: {detected_language}")
    logging.info(f"[LOG] 翻訳先言語: {target_lang}")

    # 4. 同じ言語ならそのまま返却
    if detected_language.lower() == target_lang.lower():
        logging.info("[LOG] 翻訳不要")
        return JSONResponse({
            "source_text": menu_text,
            "source_language": detected_language,
            "translated_text": menu_text
        })

    # 5. 翻訳
    try:
        translated_menu = translation_service.translate_menu(menu_text, detected_language, target_lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"翻訳エラー: {e}")
    
    logging.info(f"[LOG] 翻訳後: {translated_menu}")

    # 6. 画像に翻訳テキストを上書き
    translated_lines = translated_menu.splitlines()
    # text_boxesとtranslated_linesの数が一致しない場合は短い方に合わせる
    min_len = min(len(text_boxes), len(translated_lines))
    text_boxes = text_boxes[:min_len]
    translated_lines = translated_lines[:min_len]
    try:
        output_image_path = draw_translated_text_on_image(
            image_path=temp_image_path,
            text_boxes=text_boxes,
            translated_lines=translated_lines
        )
    except Exception as e:
        output_image_path = None
        logging.error(f"[LOG] 画像への翻訳テキスト描画に失敗: {e}")

    return JSONResponse({
        "source_text": menu_text,
        "source_language": detected_language,
        "translated_text": translated_menu,
        "output_image_path": output_image_path
    })