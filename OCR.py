import easyocr
import cv2

reader = easyocr.Reader(['ko'])  # 한국어, 영어, 숫자 인식
img_path = 'result_crop.jpg'
img = cv2.imread(img_path)
result = reader.readtext(img_path)

print(result)