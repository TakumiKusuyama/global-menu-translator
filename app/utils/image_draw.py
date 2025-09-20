from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv

def draw_translated_text_on_image(image_path, text_boxes, translated_lines, output_path=None, font_path=None, font_size=24, fill=(255,0,0)):
    # .envからフォントパスを取得（font_path未指定時のみ）
    if font_path is None:
        load_dotenv()
        font_path = os.getenv("FONT_PATH")
    """
    OCRで取得したバウンディングボックス位置に翻訳後テキストを上書きして新しい画像を保存
    Args:
        image_path (str): 元画像のパス
        text_boxes (List[dict]): [{'text', 'left', 'top', 'width', 'height'}...]
        translated_lines (List[str]): 各行の翻訳後テキスト
        output_path (str, optional): 保存先パス。未指定なら"translated_"+元画像名
        font_path (str, optional): 使用するフォントファイルパス
        font_size (int): フォントサイズ
        fill (tuple): 文字色 (R,G,B)
    Returns:
        str: 保存した画像のパス
    """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    # フォント指定（なければデフォルト）
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()
    for box, translated in zip(text_boxes, translated_lines):
        # まず元のテキスト領域を白で塗りつぶす
        draw.rectangle([
            (box['left'], box['top']),
            (box['left']+box['width'], box['top']+box['height'])
        ], fill=(255,255,255), outline=(0,255,0), width=1)  # 塗りつぶし+バウンディングボックス
        # その上に翻訳テキストを描画
        draw.text((box['left'], box['top']), translated, font=font, fill=fill)
    if not output_path:
        # プロジェクトルート/output/ディレクトリに保存
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../output'))
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        ext = os.path.splitext(image_path)[1]
        output_path = os.path.join(output_dir, f"{base_name}_translated{ext}")
    image.save(output_path)
    return output_path
