# Task 3 – Extend Attendance Repo with Gesture Recognition

## Objective
Extend the current Face Recognition Attendance System by adding Hand Gesture Detection features.

### System should be able to:
- Detect if a hand is present in the camera feed.
- Identify which hand it is (Left Hand or Right Hand).
- Count the number of fingers being shown.
- Recognize specific gestures like:
  - 👍 Thumbs Up
  - 👎 Thumbs Down

## Inputs & Outputs
**Input:** Live video frames from the Camera (same input source as face recognition).

**Output:**
- Hand Presence: "Hand Detected" or "No Hand".
- Hand Side: "Left Hand" or "Right Hand".
- Finger Count: Number of fingers shown (0–5).
- Gesture Type: "Thumbs Up", "Thumbs Down", or "Other".

## Implementation (exact files added)
- `gesture_recognition.py` — MediaPipe-based module to detect hands, handedness, count fingers, and recognize thumbs up/down.
- `execute.py` — Main runner that integrates your existing face recognition logic with gesture recognition. Contains clear placeholder where to merge existing face code.
- `architectur.md` — System architecture diagram (mermaid).
- `sequence.md` — Sequence flow (operations).
- `dfd.md` — Data flow diagram (kept from repo or updated).
- `gesture.md` — Short module description.

## How it works (summary)
1. Capture a frame from webcam (BGR). Preprocess: flip horizontally, convert to RGB for MediaPipe.
2. Face recognition runs (existing code integrated here — detect/encode/attendance).
3. Gesture recognition runs: MediaPipe Hands returns landmarks and `multi_handedness` classification.
4. For each detected hand:
   - Use handedness label from MediaPipe (Left/Right).
   - Count fingers by comparing tip vs DIP landmarks.
   - For thumbs: compare thumb tip vs thumb IP (x coordinate) depending on handedness.
   - Recognize thumbs up if thumb tip is above wrist and other fingers folded; thumbs down if below wrist and others folded.
5. Overlay results (hand label, finger count, gesture name) on frame and log to `gesture.log`.

## Dependencies
```bash
pip install mediapipe opencv-python
```

## Run
```bash
python execute.py
```

## Logging & Storage
- Gesture events appended to `gesture.log` (one entry per detection with timestamp, hand side, finger count, gesture).
- Attendance continues to be logged in `attendance.csv`.

## Notes & Validation
- Module uses normalized landmark coordinates (0..1) from MediaPipe; thresholds tuned for common camera setups but may need small adjustments.
- The code gracefully warns on missing packages and won't crash (it will show a message on the frame).
