import os
from openai import OpenAI
from app.config import SUPPORTED_LANGUAGES, MODEL_NAME_3_5_TURBO
from langdetect import detect, DetectorFactory

# langdetectの判定結果を安定化させるためのシード設定
DetectorFactory.seed = 0

"""テキストの言語を判定するサービスクラス"""
class LanguageService:
    """
    テキストの言語を判定するサービスクラス

    - detect_language: langdetectによる自動判定（言語コード返却）
    - detect_language_by_ai: OpenAI APIによる判定（言語名返却）
    """
    def __init__(self, openai_client: OpenAI):
        """
        Args:
            openai_client (OpenAI): OpenAI APIクライアント
        """
        self.openai_client = openai_client

    def detect_language(self, text: str) -> str:
        """
        langdetectによる言語判定（言語コードを返す）

        Args:
            text (str): 判定対象のテキスト

        Returns:
            str: 言語コード（例: 'ja', 'en', 'zh', 'ko' など）
        """
        return detect(text)

    def detect_language_by_ai(self, text: str) -> str:
        """
        OpenAI API (GPT) で言語名を判定（言語名を返す）

        Args:
            text (str): 判定対象のテキスト

        Returns:
            str: 言語名（例: 'Japanese', 'English', 'Chinese', 'Korean' など）
        """
        
        
        """
        次のテキストの言語を判定し、言語名のみを出力してください。
        Text: {text}
        """
        prompt = f"""
            Detect the language of the following text and output only the language name.
            Text:  {text}
        """
        try:
            # OpenAI APIによる言語判定
            response = self.openai_client.chat.completions.create(
                model=MODEL_NAME_3_5_TURBO,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"言語判定に失敗しました: {e}")