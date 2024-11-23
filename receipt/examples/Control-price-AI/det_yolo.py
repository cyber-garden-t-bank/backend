'''Локализация названия и цены с последующим распознаванием текста'''

from ultralytics import YOLO
import cv2
import easyocr
import os
import shutil
import sys

global PATH_model_det
global PATH_img_crop

def detect_yolo(img):
    model = YOLO(PATH_model_det)
    class_names = model.names
    h, w, _ = img.shape
    results = model.predict(img, conf=0.3, show=False)

    if len(results[0].boxes.xyxy) == 0:
        raise ValueError("YOLO не нашел ни одного объекта на изображении")

    boxes = results[0].boxes.xyxy.tolist()
    clss = results[0].boxes.cls.tolist()

    for box, cls in zip(boxes, clss):
        x1, y1, x2, y2 = box
        crop_object = img[int(y1):int(y2), int(x1):int(x2)]
        crop_path = os.path.join(PATH_img_crop, f"{int(cls)}.jpg")
        cv2.imwrite(crop_path, crop_object)
        print(f"Сохранен объект {cls}: {crop_path}")

def ocr(file_path): # распознавание текста
    reader = easyocr.Reader(['ru'])
    res = reader.readtext(file_path, detail =0) #detail: если поставить 1, то выведется вероятность и координаты текста на картинке
    result = ' '.join(res).strip()
    return result

def prog(PATH_img):

    # создание папки
    if not os.path.exists(PATH_img_crop):
        os.makedirs(PATH_img_crop)
        #print(f'Папка {PATH_img_crop} создана')
    else:
        r=0
        #print(f'Папка {PATH_img_crop} уже существует')

    img = cv2.imread(PATH_img)
    detect_yolo(img)

    text = ocr(PATH_img + '/' + '2.jpg')
    print(text)


    # text_price_rub = ocr(PATH_img_crop + '//' + '0.jpg') # цена (рубли)
    # text_price_cop = ocr(PATH_img_crop + '//' + '3.jpg') # цена (копейки)
    # text_name = ocr(PATH_img_crop + '//' + '1.jpg') # название

    # text = f'{text_name} {text_price_rub} {text_price_cop}'

    print(f'{text}')

    # удаление папки
    shutil.rmtree(PATH_img_crop)

if __name__ == "__main__":
    PATH_img_crop = 'image_crop'
    filename = 'download.png'
    PATH_model_det = 'yolo_8n_price.pt'

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Изображение {filename} не найдено")

    os.makedirs(PATH_img_crop, exist_ok=True)
    # prog(filename)
    text = ocr(file_path=filename)
    print(text)