import cv2

# 打开默认摄像头（0 代表第一个摄像头）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ 摄像头打开失败，请检查设备或权限。")
else:
    print("✅ 摄像头已打开，按 q 退出。")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ 无法读取帧。")
        break

    # 显示摄像头画面
    cv2.imshow("Camera Test", frame)

    # 按 q 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()