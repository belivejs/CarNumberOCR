from ultralytics import YOLO
import cv2
import os

# 학습된 모델 로드
model = YOLO('runs/detect/train/weights/best.pt')

# 이미지로 예측
results = model.predict('test_car.jpg', conf=0.7)

# 결과 시각화 (바운딩 박스 그려진 이미지 표시)
results[0].show()

# 또는 저장
os.makedirs('images', exist_ok=True)
results[0].save('images/result.jpg')
