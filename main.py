# main.py
# Author: Jiaying Zong
# Function: Read camera input → Detect hand position → Send OSC to TouchDesigner

import cv2
import mediapipe as mp
from pythonosc import udp_client
import time
from collections import deque
import numpy as np

# ============ 初始化部分 ============
# OSC 连接到 TD（端口可让队友确认）
client = udp_client.SimpleUDPClient("127.0.0.1", 8000)

# 初始化摄像头（0为默认摄像头）
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print(" 无法打开摄像头，请检查设置。")
    exit()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# 平滑缓存队列（防止抖动）
smooth_x = deque(maxlen=5)
smooth_y = deque(maxlen=5)

print(" 系统初始化完成。按 Q 退出。")
print("🔗 发送到: 127.0.0.1:8000 | 地址路径: /handpos [x, y]")

# ============  主循环 ============
while True:
    ret, frame = cap.read()
    if not ret:
        print(" 无法读取摄像头帧。")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, c = frame.shape
            x_sum, y_sum, count = 0, 0, 0
            for lm in handLms.landmark:
                x_sum += lm.x
                y_sum += lm.y
                count += 1
            x_avg = x_sum / count
            y_avg = y_sum / count

            # 平滑化
            smooth_x.append(x_avg)
            smooth_y.append(y_avg)
            x_smooth = np.mean(smooth_x)
            y_smooth = np.mean(smooth_y)

            # 发送 OSC
            client.send_message("/handpos", [float(x_smooth), float(y_smooth)])
            print(f"📤 Sent to TD: /handpos [{x_smooth:.2f}, {y_smooth:.2f}]")

            # 可视化手部
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Camera → OSC (TD Bridge)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()