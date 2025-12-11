from ultralytics import YOLO

# 첫 실행 시 자동으로 yolov8s.pt 다운로드됨
model = YOLO('yolov8s.pt')

results = model.train(
    data='car_plate/data.yaml',
    epochs=100,
    batch=8,
    device='mps'
)
