from PIL import Image
import pytesseract
from app.config import SUPPORTED_LANGUAGES

""" 画像からテキストを抽出するサービスクラス """
class OCRService:

    
    def __init__(self, lang: str = None):
        """
        OCRServiceの初期化
        Args:
            lang (str, optional): Tesseract用の言語指定文字列。未指定ならSUPPORTED_LANGUAGESから自動生成。
        """
        # SUPPORTED_LANGUAGESからTesseract用のlang文字列を生成
        if lang is None:
            # 言語コードをTesseract用に変換（例: ja→jpn, en→eng, zh→chi_sim, ko→kor など）
            language_map = {"ja": "jpn", "en": "eng", "zh": "chi_sim", "ko": "kor"}
            # サポート言語(SUPPORTED_LANGUAGES)からTesseract用の言語文字列を生成
            tesseract_langs = [language_map.get(code, code) for code in SUPPORTED_LANGUAGES]
            # Tesseract用の言語文字列を連結
            self.tesseract_langs = "+".join(tesseract_langs)
        else:
            self.tesseract_langs = lang

    def extract_text(self, image_path: str) -> str:
        """
        画像ファイルからテキストを抽出し、前処理して返す

        Args:
            image_path (str): 画像ファイルのパス

        Returns:
            str: 前処理済みのテキスト
        """
        try:
            # 画像を読み込む
            image = Image.open(image_path)
            # 画像からテキストを抽出
            extracted_image_text = pytesseract.image_to_string(image, lang=self.tesseract_langs)
            # 抽出したテキストを前処理して返す
            return extracted_image_text
        except Exception as e:
            raise RuntimeError(f"OCR処理に失敗しました: {e}")
        
        
    def extract_text_with_boxes(self, image_path: str):
        """
        画像ファイルから各テキスト行のバウンディングボックスとテキストを抽出

        Args:
            image_path (str): 画像ファイルのパス

        Returns:
            List[dict]: [{'text': str, 'left': int, 'top': int, 'width': int, 'height': int}, ...]
        """
        try:
            image = Image.open(image_path)
            # pytesseractのimage_to_dataで詳細なOCR情報を取得
            ocr_data = pytesseract.image_to_data(image, lang=self.tesseract_langs, output_type=pytesseract.Output.DICT)
            results = []
            n_boxes = len(ocr_data['level'])
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                if text:
                    results.append({
                        'text': text,
                        'left': ocr_data['left'][i],
                        'top': ocr_data['top'][i],
                        'width': ocr_data['width'][i],
                        'height': ocr_data['height'][i]
                    })
            return results
        except Exception as e:
            raise RuntimeError(f"OCRバウンディングボックス抽出に失敗しました: {e}")

    def preprocess_ocr_text(self, text: str) -> str:
        """
        OCR後のテキストを前処理（空行除去・ノイズ除去など）

        Args:
            text (str): OCRで抽出したテキスト

        Returns:
            str: 前処理済みのテキスト
        """
        # 空行除去・前後空白除去
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        # ノイズ除去: 1文字以下の行や英数字が含まれない行を除外
        lines = [line for line in lines if len(line) > 1 and any(c.isalnum() for c in line)]
        return "\n".join(lines)