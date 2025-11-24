import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def detect_hand_position(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            x = sum([lm.x for lm in hand.landmark]) / len(hand.landmark)
            y = sum([lm.y for lm in hand.landmark]) / len(hand.landmark)
            return x, y
    return None