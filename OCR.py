import easyocr
import cv2

reader = easyocr.Reader(['ko'])  # 한국어, 영어, 숫자 인식

def run_ocr(img_path='result_crop.jpg'):
    try:
        result = reader.readtext(img_path)
        return result[0][1]
    except:
        return "인식 실패"

if __name__ == "__main__":
    print(run_ocr())
