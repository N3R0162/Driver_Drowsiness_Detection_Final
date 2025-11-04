import torch
import sys
print(torch.cuda.is_available())
# Detect OS:
import cv2
if sys.platform.startswith('win'):
    os_name = 'Windows'
elif sys.platform.startswith('linux'):
    os_name = 'Linux'
else:
    os_name = 'Other'

print(f"Operating System: {os_name}")

video_file = 0  # Default webcam (or use 1, 2, 3 for other cameras)
def play_webcam():
    # Normal Camera - Windows uses integer index
    source_webcam = 0  # Change from "/dev/video0" to 0
    # Jetson Nano CSI Camera
    # pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'

    # Run webcam test
    cap = cv2.VideoCapture(source_webcam)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    ret, frame = cap.read()
    if ret:
        print("Webcam is working correctly.")
    else:
        print("Error: Could not read frame from webcam.")

play_webcam()