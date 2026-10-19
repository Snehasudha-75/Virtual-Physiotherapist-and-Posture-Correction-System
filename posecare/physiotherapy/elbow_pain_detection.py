import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import threading

# ================= INIT =================
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)
draw = mp.solutions.drawing_utils

engine = pyttsx3.init()
engine.setProperty('rate', 160)

last_state = ""
last_time = 0

good_frames = 0
total_frames = 0

# ================= VOICE =================
def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# ================= ANGLE FUNCTION =================
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    angle = np.degrees(
        np.arccos(
            np.clip(
                np.dot(a-b, c-b) /
                (np.linalg.norm(a-b) * np.linalg.norm(c-b)),
                -1.0, 1.0
            )
        )
    )
    return angle

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(image)

    feedback = "No person detected"
    state = "NONE"

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                    lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
        elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                 lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
        wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                 lm[mp_pose.PoseLandmark.RIGHT_WRIST].y]

        angle = calculate_angle(shoulder, elbow, wrist)
        total_frames += 1

        if 80 <= angle <= 110:
            feedback = "✅ Good elbow posture"
            state = "GOOD"
            good_frames += 1
            color = (0, 255, 0)
        elif 60 <= angle < 80 or 110 < angle <= 130:
            feedback = "⚠ Adjust elbow position"
            state = "ADJUST"
            color = (0, 255, 255)
        else:
            feedback = "❌ Elbow strain detected"
            state = "BAD"
            color = (0, 0, 255)

        cv2.putText(frame, f"Elbow Angle: {int(angle)}°",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    
    if state != last_state and time.time() - last_time > 4:
        if state == "BAD":
            speak("Elbow strain detected. Relax your arm")
        elif state == "ADJUST":
            speak("Adjust your elbow position")
        elif state == "GOOD":
            speak("Good elbow posture")
        last_state = state
        last_time = time.time()

    cv2.putText(frame, feedback, (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("PoseCare - Elbow Pain Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

posture_score = int((good_frames / total_frames) * 100) if total_frames else 0

with open("posture_score.txt", "w") as f:
    f.write(str(posture_score))

print("Elbow posture score:", posture_score)
