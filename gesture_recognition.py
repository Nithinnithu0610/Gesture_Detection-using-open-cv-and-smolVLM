import cv2
#Imports OpenCV, used for capturing video, processing images, and drawing on frames.
import mediapipe as mp
#Imports MediaPipe, used for hand/pose/face detection and tracking in real-time.
import csv
#Python built-in module for reading and writing CSV files (useful for logging hand landmarks or gestures).
import os
#Python built-in module for file and folder operations (creating directories, checking file paths, etc.).
import argparse
#Python built-in module for parsing command-line arguments (like specifying which hand to track or which dataset folder to use).
from datetime import datetime

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def fingers_up(lm, handedness):
    """Return list of 5 values [thumb, index, middle, ring, pinky], 1 if up else 0"""
    fingers = []

    # Thumb
    if handedness == "Right":
        fingers.append(1 if lm[4].x < lm[3].x else 0)
    else:
        fingers.append(1 if lm[4].x > lm[3].x else 0)

    # Other fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lm[tip].y < lm[tip - 2].y else 0)

    return fingers


def classify_gesture(fingers, lm, handedness):
    """Classify gesture from finger states"""
    thumb, index, middle, ring, pinky = fingers

    # Thumbs Up
    if thumb == 1 and index == 0 and middle == 0 and ring == 0 and pinky == 0:
        if lm[4].y < lm[3].y:  # y smaller = up
            return f"{handedness}_Thumbs_Up"
        elif lm[4].y > lm[3].y:  # y bigger = down
            return f"{handedness}_Thumbs_Down"

    # Index + Thumb open
    if thumb == 1 and index == 1 and middle == 0 and ring == 0 and pinky == 0:
        return f"{handedness}_IndexThumb_Open"

    # Hand Down (fist)
    if sum(fingers) == 0:
        return f"{handedness}_Hand_Down"

    # Open hand
    if sum(fingers) == 5:
        return f"{handedness}_Open_Hand"

    return f"{handedness}_{sum(fingers)}Fingers"


def main(args):
    os.makedirs(args.out_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    cap = cv2.VideoCapture(0 if not args.input else args.input)
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    logfile = open("logs/gesture_outputs.log", "w", newline="")
    writer = csv.writer(logfile)
    writer.writerow(["timestamp", "frame_id", "hand", "gesture"])

    saved_frames = {}  # Track frames saved per gesture
    frame_id = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_id += 1
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)

            gestures = []

            if res.multi_hand_landmarks:
                for hand_landmarks, hand_handedness in zip(
                    res.multi_hand_landmarks, res.multi_handedness
                ):
                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
                    hand_label = hand_handedness.classification[0].label
                    lm = hand_landmarks.landmark
                    finger_state = fingers_up(lm, hand_label)
                    gesture = classify_gesture(finger_state, lm, hand_label)
                    gestures.append((hand_label, gesture))

                    # Log
                    writer.writerow(
                        [datetime.now().isoformat(), frame_id, hand_label, gesture]
                    )

                    # Save up to 3 frames per gesture
                    if gesture not in saved_frames:
                        saved_frames[gesture] = 0
                    if saved_frames[gesture] < 3:
                        out_path = os.path.join(
                            args.out_dir, f"{gesture}_{frame_id}.jpg"
                        )
                        cv2.imwrite(out_path, frame)
                        saved_frames[gesture] += 1

                    # Show text
                    cv2.putText(
                        frame,
                        gesture,
                        (10, 100 if hand_label == "Right" else 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 255, 0),
                        3,
                    )

            cv2.imshow("Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        logfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="", help="Video path; leave empty for webcam")
    parser.add_argument("--out_dir", default="frames", help="Folder to save frames")
    args = parser.parse_args()
    main(args)
