import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, PhotoImage
from PIL import Image, ImageTk
from OCR import run_ocr

root = ttk.Window(themename="flatly") 
root.title("License Plate Detection Result")
root.geometry("1200x600") 
root.resizable(False, False)

def update_results():

    
    # 1. 원본 탐지 이미지 로드 (result.jpg)
    try:
        img = Image.open("images/result.jpg")
        # GUI 크기에 맞춰 리사이즈 (가로 350px 기준)
        w, h = img.size
        ratio = 350 / w
        new_h = int(h * ratio)
        img = img.resize((350, new_h), Image.Resampling.LANCZOS)
        
        tk_img = ImageTk.PhotoImage(img)
        detection_label.config(image=tk_img, text="") # 텍스트 제거
        detection_label.image = tk_img # 참조 유지
    except Exception as e:
        print(f"Failed to load image (result.jpg): {e}")

    # 2. 크롭된 번호판 이미지 로드 (result_crop.jpg)
    try:
        img_crop = Image.open("images/result_crop.jpg")
        w, h = img_crop.size
        ratio = 350 / w
        new_h = int(h * ratio)
        img_crop = img_crop.resize((350, new_h), Image.Resampling.LANCZOS)
        
        tk_img_crop = ImageTk.PhotoImage(img_crop)
        cropped_label.config(image=tk_img_crop, text="")
        cropped_label.image = tk_img_crop
    except Exception as e:
        print(f"Failed to load image (result_crop.jpg): {e}")

    # 3. 번호판 텍스트 로드
    try:
        ocr_result = run_ocr()
        plate_number_label.config(text=ocr_result)
    except Exception as e:
        print(f"Failed to load OCR text: {e}")

# --- 상단 버튼 영역 (헤더) ---
header_frame = ttk.Frame(root, padding=10)
header_frame.pack(fill='x', padx=20, pady=(10, 5))

ttk.Label(header_frame, text="License Plate Detection Program", font=("Helvetica", 18, "bold"), bootstyle="primary").pack(side='left')

# --- 메인 결과 영역 (3분할) ---
main_frame = ttk.Frame(root, padding="0 20 20 20")
main_frame.pack(expand=True, fill='both')

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)



# COLUMN1: 탐지 사진 (원본 + Bounding Box)
frame_detection = ttk.Labelframe(main_frame, text="1. Original Image (Detection Area)", padding="10", bootstyle="primary")
frame_detection.grid(row=0, column=0, padx=20, sticky="nsew")

detection_label = ttk.Label(
    frame_detection, 
    text="Waiting for image load...", 
    anchor="center",
    bootstyle="inverse-primary"
)
detection_label.pack(expand=True, fill='both', ipady=120) 



# COLUMN2: 번호판 사진 (추출 이미지)
frame_cropped = ttk.Labelframe(main_frame, text="2. Cropped Plate Area", padding="10", bootstyle="info")
frame_cropped.grid(row=0, column=1, padx=20, sticky="nsew")

cropped_label = ttk.Label(
    frame_cropped, 
    text="Cropped Plate Image", 
    anchor="center",
    bootstyle="inverse-info"
)
cropped_label.pack(expand=True, fill='both', ipady=120)



# COLUMN3: 최종 인식 텍스트 
frame_result = ttk.Labelframe(main_frame, text="3. Final OCR Result", padding="20", bootstyle="success")
frame_result.grid(row=0, column=2, padx=20, sticky="nsew")

ttk.Label(
    frame_result, 
    text="[ Result ]", 
    font=("Helvetica", 13, "bold"),
    bootstyle="success"
).pack(pady=(10, 5))

plate_number_label = ttk.Label(
    frame_result, 
    text="----", 
    font=("Arial", 30, "bold"), 
    bootstyle="inverse-success"
)
plate_number_label.pack(pady=20, fill='x', padx=10)

# 앱 실행 시 자동으로 결과 업데이트 수행
update_results()

root.mainloop()