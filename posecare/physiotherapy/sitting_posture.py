# import cv2
# import mediapipe as mp
# import numpy as np
# import pyttsx3

# engine = pyttsx3.init()
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()
# draw = mp.solutions.drawing_utils

# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     angle = np.degrees(
#         np.arccos(
#             np.dot(a-b, c-b) /
#             (np.linalg.norm(a-b) * np.linalg.norm(c-b))
#         )
#     )
#     return angle

# cap = cv2.VideoCapture(0)
# last_feedback = ""

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = pose.process(image)

#     feedback = "No person detected"

#     if result.pose_landmarks:
#         lm = result.pose_landmarks.landmark

#         shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
#                     lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
#         hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x,
#                lm[mp_pose.PoseLandmark.LEFT_HIP].y]
#         ear = [lm[mp_pose.PoseLandmark.LEFT_EAR].x,
#                lm[mp_pose.PoseLandmark.LEFT_EAR].y]

#         angle = calculate_angle(shoulder, hip, ear)

#         if angle < 160:
#             feedback = "Wrong posture. Sit straight"
#         else:
#             feedback = "Good posture"

#         if feedback != last_feedback:
#             engine.say(feedback)
#             engine.runAndWait()
#             last_feedback = feedback

#         cv2.putText(frame, f"Angle: {int(angle)}",
#                     (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

#     draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#     cv2.putText(frame, feedback,
#                 (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

#     cv2.imshow("PoseCare - Sitting Posture", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import threading
from PIL import Image

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

# ================= LOAD GIF =================
gif = Image.open("giphy1.gif")
gif_frames = []

try:
    while True:
        frame = gif.copy().convert("RGB")
        gif_frames.append(np.array(frame))
        gif.seek(len(gif_frames))
except EOFError:
    pass

gif_index = 0

# ================= VOICE (NON BLOCKING) =================
def speak(text):
    threading.Thread(
        target=lambda: engine.say(text) or engine.runAndWait()
    ).start()

# ================= ANGLE =================
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
    state = "NO_PERSON"

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        ear = [lm[mp_pose.PoseLandmark.LEFT_EAR].x,
               lm[mp_pose.PoseLandmark.LEFT_EAR].y]
        shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                    lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x,
               lm[mp_pose.PoseLandmark.LEFT_HIP].y]

        angle = calculate_angle(ear, shoulder, hip)
        total_frames += 1

        if angle < 140:
            feedback = "❌ Bad posture"
            state = "BAD"
        elif angle < 160:
            feedback = "⚠ Adjust posture"
            state = "ADJUST"
        else:
            feedback = "✅ Good posture"
            state = "GOOD"
            good_frames += 1

        draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f"Neck Angle: {int(angle)}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2)

    # ================= VOICE CONTROL =================
    if state != last_state and time.time() - last_time > 3:
        if state == "BAD":
            speak("Your posture is wrong. Follow the posture shown.")
        elif state == "ADJUST":
            speak("Adjust your posture.")
        elif state == "GOOD":
            speak("Good posture. Keep it up.")
        elif state == "NO_PERSON":
            speak("No person detected. Sit in front of the camera.")

        last_state = state
        last_time = time.time()

    cv2.putText(frame, feedback,
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 0, 255), 2)

    # ================= SHOW GIF =================
    gif_frame = gif_frames[gif_index]
    gif_frame = cv2.resize(gif_frame, (300, 500))
    gif_index = (gif_index + 1) % len(gif_frames)

    cv2.imshow("Correct Posture Instruction", gif_frame)
    cv2.imshow("PoseCare - Live Detection", frame)

    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

# ================= SAVE SCORE =================
cap.release()
cv2.destroyAllWindows()

score = int((good_frames / total_frames) * 100) if total_frames else 0

with open("posture_score.txt", "w") as f:
    f.write(str(score))

print("Posture Score:", score)
