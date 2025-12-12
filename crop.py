import cv2
import os
from ultralytics import YOLO

# -------------------------------------------------------------------
# [Configuration] 모델 경로 및 저장 파일명 설정
# 팀원 환경에 맞게 MODEL_PATH가 정확한지 확인이 필요합니다.
# -------------------------------------------------------------------
MODEL_PATH = 'runs/detect/train/weights/best.pt'
SAVE_NAME = "result_crop.jpg"

def crop_plate(image_path):
    """
    YOLOv8 모델을 사용하여 이미지 내의 번호판을 탐지하고,
    해당 영역(ROI)을 크롭(Crop)하여 파일로 저장합니다.

    Args:
        image_path (str): 입력할 원본 이미지의 파일 경로

    Returns:
        str: 저장된 크롭 이미지의 경로 (탐지 실패 시 None 반환)
    """
    
    # 1. 모델 가중치(Weights) 파일 존재 여부 검증
    if not os.path.exists(MODEL_PATH):
        print(f"[Error] 모델 파일을 찾을 수 없습니다. 경로 확인 필요: {MODEL_PATH}")
        return None

    # 2. 모델 로드 (Load Model)
    # best.pt 가중치를 사용하여 YOLO 객체 생성
    print(f"[Info] 모델 로딩 중... ({MODEL_PATH})")
    model = YOLO(MODEL_PATH)

    # 3. 이미지 읽기 (Image Read)
    img = cv2.imread(image_path)
    if img is None:
        print(f"[Error] 이미지 파일을 읽을 수 없습니다. 경로: {image_path}")
        return None

    # 4. 추론 (Inference) 수행
    # conf: 신뢰도 임계값 (0.25 이상일 때만 탐지)
    print("[Info] 객체 탐지 수행 중...")
    results = model.predict(source=img, save=False, conf=0.25, verbose=False)

    # 5. 결과 후처리 (Post-processing)
    for result in results:
        boxes = result.boxes
        
        # 탐지된 객체가 없는 경우 예외 처리
        if len(boxes) == 0:
            print("[Warning] 번호판이 탐지되지 않았습니다.")
            return None

        # 가장 신뢰도(Confidence)가 높은 첫 번째 객체의 좌표 추출
        # xyxy: [x_min, y_min, x_max, y_max] 형식
        box = boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        print(f"[Info] 번호판 좌표 감지: x({x1}~{x2}), y({y1}~{y2})")

        # 6. 관심 영역(ROI) 추출 및 저장
        # Numpy Slicing을 통해 이미지 크롭 진행
        cropped_img = img[y1:y2, x1:x2]
        
        try:
            cv2.imwrite(SAVE_NAME, cropped_img)
            print(f"[Success] 크롭 이미지 저장 완료: {SAVE_NAME}")
            return SAVE_NAME
        except Exception as e:
            print(f"[Error] 파일 저장 중 오류 발생: {e}")
            return None

# -------------------------------------------------------------------
# [Main Execution] 테스트 실행 영역
# 이 파일이 직접 실행될 때만 동작하며, import 시에는 실행되지 않습니다.
# -------------------------------------------------------------------
if __name__ == "__main__":
    # 테스트용 이미지 경로 설정
    test_photo = "datasets/test/images/20240923033528_006-6974_CAM_1_jpg.rf.0a6f5c09cc25f0b3a7cc864f73d92dbd.jpg"
    
    # 함수 호출 및 결과 확인
    saved_file = crop_plate(test_photo)

    if saved_file:
        # 결과 시각화 (Visualization)
        img_view = cv2.imread(saved_file)
        cv2.imshow("Detection Result", img_view)
        
        print("아무 키나 누르면 종료됩니다.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
