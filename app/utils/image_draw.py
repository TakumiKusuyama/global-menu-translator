def draw_translated_text_on_image(image_path, text_boxes, translated_lines, output_path=None, font_path=None, font_size=24, fill=(255,0,0)):

from PIL import Image, ImageDraw, ImageFont
import os

class ImageTextDrawer:
    """
    画像上にテキストを描画するユーティリティクラス
    """
    def __init__(self, font_path=None, font_size=24, fill=(255,0,0)):
        self.font_path = font_path
        self.font_size = font_size
        self.fill = fill

    def draw_translated_text_on_image(self, image_path, text_boxes, translated_lines, output_path=None):
        """
        OCRで取得したバウンディングボックス位置に翻訳後テキストを上書きして新しい画像を保存
        Args:
            image_path (str): 元画像のパス
            text_boxes (List[dict]): [{'text', 'left', 'top', 'width', 'height'}...]
            translated_lines (List[str]): 各行の翻訳後テキスト
            output_path (str, optional): 保存先パス。未指定なら"translated_"+元画像名
        Returns:
            str: 保存した画像のパス
        """
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        # フォント指定（なければデフォルト）
        if self.font_path and os.path.exists(self.font_path):
            font = ImageFont.truetype(self.font_path, self.font_size)
        else:
            font = ImageFont.load_default()
        for box, translated in zip(text_boxes, translated_lines):
            # テキストの左上座標に描画
            draw.rectangle([
                (box['left'], box['top']),
                (box['left']+box['width'], box['top']+box['height'])
            ], fill=None, outline=(0,255,0), width=1)  # バウンディングボックスも描画（デバッグ用）
            draw.text((box['left'], box['top']), translated, font=font, fill=self.fill)
        if not output_path:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_translated{ext}"
        image.save(output_path)
        return output_path
