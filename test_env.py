# test_env.py
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# 環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("APIキーを取得しました:", api_key[:10] + "..." )  # 最初の10文字だけ表示
else:
    print("APIキーが見つかりません")
