from PIL import Image
from tesserocr import PyTessBaseAPI

image_path = 'download.png'

# Открываем изображение
image = Image.open(image_path)

# Используем API Tesserocr
with PyTessBaseAPI() as api:
    api.SetImage(image)
    extracted_text = api.GetUTF8Text()

print("Extracted Text:")
print(extracted_text)
