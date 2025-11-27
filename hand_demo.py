import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 初始化 Hands 模型
hands = mp_hands.Hands(
    max_num_hands=1,               # 最多识别一只手
    min_detection_confidence=0.5,  # 检测置信度
    min_tracking_confidence=0.5    # 跟踪置信度
)

cap = cv2.VideoCapture(0)  # 如果你有多个摄像头可以改成 1、2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 镜像一下，像自拍
    frame = cv2.flip(frame, 1)

    # Mediapipe 要用 RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 在画面上画出关键点
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("MediaPipe Hands", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # 按 ESC 退出
        break

cap.release()
cv2.destroyAllWindows()