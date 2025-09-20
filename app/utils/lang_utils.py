# 言語コードから言語名への変換辞書
LANG_CODE_TO_NAME = {
    "en": "English",
    "ja": "Japanese",
    "zh": "Chinese",
    "ko": "Korean",
    # 必要に応じて追加
}

# 言語コードを言語名に変換するユーティリティ
def lang_code_to_name(code: str) -> str:
    return LANG_CODE_TO_NAME.get(code, code)
