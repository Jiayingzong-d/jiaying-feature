import cv2
import mediapipe as mp
import numpy as np

from pythonosc import udp_client
client = udp_client.SimpleUDPClient("127.0.0.1", 8000)
# =======================================

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 打开摄像头，0 是默认摄像头
cap = cv2.VideoCapture(0)

# 这里可以调参数：max_num_hands=1 只追一只手
with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("⚠️ 没有捕获到摄像头画面")
            break

        # OpenCV 读进来是 BGR，需要先转成 RGB 给 Mediapipe 用
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        # 再转回 BGR，用来显示
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        hand_center = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 画关键点和骨架
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 计算手的平均坐标（归一化 0~1）
                xs = [lm.x for lm in hand_landmarks.landmark]
                ys = [lm.y for lm in hand_landmarks.landmark]
                cx, cy = float(np.mean(xs)), float(np.mean(ys))
                hand_center = (cx, cy)

                # 在图像上画一个圆点
                h, w, _ = image.shape
                px, py = int(cx * w), int(cy * h)
                cv2.circle(image, (px, py), 10, (0, 255, 0), -1)

                # 显示坐标文字
                cv2.putText(image, f"x:{cx:.2f} y:{cy:.2f}",
                            (px + 10, py - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # ===== 如果你之后想发 OSC 给 UE，可以在这里加 =====
                client.send_message("/handpos", [cx, cy])

        cv2.imshow('Hand Tracking (Pure Python)', image)

        # 按 q 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
