# Sequence Diagram (Attendance + Gesture Process)

```mermaid
sequenceDiagram
    participant User as Student/Employee
    participant Camera
    participant FR as Face Recognition
    participant DB as Stored Encodings
    participant AM as Attendance Manager
    participant CSV as Attendance.csv
    participant Log as performance.log
    participant GR as Gesture Recognition
    participant GL as gesture.log

    User ->> Camera: Appears in front of camera
    Camera ->> FR: Capture frame (face path)
    Camera ->> GR: Capture frame (gesture path)

    FR ->> DB: Compare encoding with known faces
    DB -->> FR: Return match (if found)
    FR ->> AM: Send recognition result
    AM ->> CSV: Mark attendance (Name, Time)
    AM ->> Log: Record system performance
    CSV -->> AM: Save entry
    Log -->> AM: Save log

    GR ->> GR: Detect hand landmarks
    GR ->> GR: Identify Left/Right hand
    GR ->> GR: Count extended fingers
    GR ->> GR: Recognize thumbs up/down
    GR ->> GL: Save gesture event (time, hand, fingers, gesture)
    GL -->> GR: Confirm log saved
