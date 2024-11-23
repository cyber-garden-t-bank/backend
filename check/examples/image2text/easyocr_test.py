import easyocr

# Создаем ридер EasyOCR
reader = easyocr.Reader(['en', 'ru'])  # Укажите языки

# Анализируем изображение
results = reader.readtext('download.png')

# Выводим текст
for result in results:
    print(result[1])  # result[1] содержит распознанный текст
