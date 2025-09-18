import os
import logging
from openai import OpenAI
from app.config import DEFAULT_SOURCE_LANG, DEFAULT_TARGET_LANG, SUPPORTED_LANGUAGES, MODEL_NAME_4_0_O



"""メニュー翻訳サービスクラス"""
class TranslationService:
    def __init__(self, client: OpenAI):
        self.client = client

    def translate_menu(self, menu_text: str, source_lang: str, target_lang: str) -> str:
        """
        メニューの各行を個別に翻訳し、すべての行を結合して返す

        Args:
            menu_text (str): OCRで抽出したメニュー全体のテキスト
            source_lang (str): 翻訳元言語コード
            target_lang (str): 翻訳先言語コード

        Returns:
            str: 各行を翻訳した結果を結合したテキスト
        """
        # 空行や余分な空白を除去し、1行ずつリスト化
        menu_lines = [line.strip() for line in menu_text.splitlines() if line.strip()]
        translated_lines = []

        for original_line in menu_lines:

            # プロンプト
            """
            あなたはプロのメニューローカライザーです。
            次のメニュー項目を{source_lang}から{target_lang}に翻訳してください。
            ・自然で観光客にわかりやすい表現にしてください。
            ・価格や分量はそのままにしてください。
            ・有名な料理名があればそれを使ってください。
            ・ユニークな料理にはカッコで短い説明を加えてください。
            ・「料理名 - 価格」の形式で1行ずつ出力してください。
            - Add short explanations in parentheses for unique dishes.
            - Output in the format: Dish Name - Price
            """
            prompt = f"""
                You are a professional menu localizer.
                Translate the following menu item from {source_lang} to {target_lang}.
                - Make it natural and tourist-friendly.
                - Keep prices and quantities unchanged.
                - Use well-known dish names if available.

                Text:
                {original_line}
            """
            try:
                # OpenAI API呼び出し
                response = self.client.chat.completions.create(
                    model=MODEL_NAME_4_0_O,
                    messages=[{"role": "user", "content": prompt}]
                )
                # 翻訳結果を取得
                translated_line = response.choices[0].message.content.strip()
                logging.debug(f"[LOG] 翻訳後: {translated_line}")
                # 翻訳結果をリストに追加
                translated_lines.append(translated_line)
            except Exception as e:
                logging.error(f"[LOG] 翻訳失敗: {original_line} ({e})")
                translated_lines.append(f"[翻訳失敗]: {original_line}")

        # 各行の翻訳結果を改行で結合して返す
        return "\n".join(translated_lines)