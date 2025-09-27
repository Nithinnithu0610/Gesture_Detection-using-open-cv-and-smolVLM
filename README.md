# Task 3 – Gesture Recognition

## 📌 Overview
This project implements a **gesture recognition system** using OpenCV / MediaPipe along with a secondary module using **SmolVLM**.  
It captures gestures, saves input frames, logs detection outputs, monitors system usage, and provides benchmark comparisons.  

This repository satisfies the reviewer’s requirements:
- Logs CPU & memory usage
- Logs gesture detection outputs
- Saves at least 3 frames for each gesture
- Provides requirements.txt for dependencies
- Implements and compares a second gesture detection module (SmolVLM)
- Includes benchmark results and diagrams/documentation

---

## 📂 Repository Structure

```
Gesture-recognition/
├── README.md
├── requirements.txt
├── execute.py
├── gesture_recognition.py
├── system_monitor.py
├── smolvlm_module/
│   └── smolvlm_module.py
├── benchmarks/
│   ├── run_benchmarks.py
│   └── results_summary.csv
├── frames/
│   ├── right_index_thumb_open_1.png
│   ├── ...
│   └── both_hands_3.png
├── logs/
│   ├── gesture_outputs.log
│   └── system_usage.log
├── docs/
│   ├── architecture.md
│   ├── dfd.md
│   ├── sequence.md
│   ├── gesture.md
│   └── task.md
```

---

## 🛠️ Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the main gesture recognition (OpenCV + MediaPipe):

```bash
python execute.py --input sample_video.mp4 --out_dir ./outputs --use_video
```

Run the SmolVLM module:

```bash
python smolvlm_module/smolvlm_module.py --input sample_video.mp4 --out_dir ./outputs_smolvlm
```

Run benchmarks:

```bash
python benchmarks/run_benchmarks.py --input_dir ./sample_videos --output benchmarks/results_summary.csv
```

---

## 🧪 Supported Gestures

1. Right hand – index finger & thumb open  
2. Left hand – down  
3. Right hand – thumbs up  
4. Right hand – down  
5. Both hands simultaneously:  
   - Right hand → thumbs up  
   - Left hand → thumbs down  

At least **3 frames per gesture** are included under `frames/`.

---

## 📊 Results & Logs

- Gesture detections → `logs/gesture_outputs.log`  
- System usage (CPU, memory) → `logs/system_usage.log`  
- Benchmark results → `benchmarks/results_summary.csv`  

---

## 📖 Documentation

Detailed design docs are in `docs/`:
- `architecture.md`
- `dfd.md`
- `sequence.md`
- `gesture.md`
- `task.md`

---

## 👨‍💻 Author
**Nithin H**
