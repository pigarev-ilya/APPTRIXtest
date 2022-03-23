from PIL import Image
from django.conf import settings


def add_watermark(input_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open(f'{str(settings.MEDIA_ROOT)}/watermark.png')
    base_image.paste(watermark, (10, 10), mask=watermark)
    base_image.save(f'{settings.MEDIA_ROOT}/{input_image_path}')
