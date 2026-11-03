# 🤖 AI Hand Gesture Recognition & GestureMusic

A real-time AI-powered hand gesture recognition system built using **Computer Vision, Machine Learning, and MediaPipe**. The project recognizes hand gestures through a webcam and converts them into computer and media-control actions.

The project also includes **GestureMusic**, a web-based application that integrates the existing hand gesture recognition pipeline with the Apple Music Windows application, enabling touch-free music control.

---

## 📌 Project Overview

This project explores touch-free human-computer interaction using hand gestures.

A webcam captures hand movements, MediaPipe detects hand landmarks, and a trained machine learning model classifies the gestures. The predicted gestures are processed using confidence-based filtering and gesture smoothing before triggering the corresponding actions.

The project consists of two components:

**1. AI Hand Gesture Recognition**
- Real-time hand detection and landmark extraction.
- Machine learning-based gesture classification.
- Confidence-based prediction.
- Gesture smoothing.
- Computer and media control.

**2. GestureMusic**
- Web-based gesture control interface.
- FastAPI backend.
- Real-time WebSocket communication.
- Webcam frame processing.
- Apple Music Windows media-key integration.

---

## 🔄 System Architecture

### Original AI Hand Gesture Recognition

```text
Webcam
   ↓
Hand Detection (MediaPipe)
   ↓
Hand Landmark Extraction
   ↓
Feature Extraction
   ↓
Machine Learning Model
   ↓
Confidence-Based Prediction
   ↓
Gesture Smoothing
   ↓
Gesture Classification
   ↓
Computer / Media Control
```

### GestureMusic Architecture

```text
Webcam
   ↓
Frontend (HTML, CSS, JavaScript)
   ↓
WebSocket Connection
   ↓
FastAPI Backend
   ↓
OpenCV Frame Processing
   ↓
MediaPipe Hand Detection
   ↓
Feature Extraction
   ↓
Trained ML Model
   ↓
Confidence Filtering
   ↓
Gesture Smoothing
   ↓
Apple Music Media Controller
   ↓
Windows Media Controls
```

---

# 🧠 AI & Machine Learning Techniques

## 1. Hand Landmark Detection

The system uses **MediaPipe Hand Landmarker** to detect a hand and identify its key landmark points.

These landmarks represent the geometric structure of the hand and provide the information required for gesture recognition.

## 2. Feature Extraction

The detected hand landmarks are transformed into numerical features.

The feature extraction pipeline uses wrist-relative landmark coordinates to generate a structured feature representation for the machine learning model.

This allows the model to learn hand-pose patterns independently of the original webcam image.

## 3. Machine Learning Classification

A supervised machine learning classification model is trained using the extracted landmark features.

The model learns the relationship between hand landmark patterns and predefined gesture classes.

### Gesture Classes

| Gesture | Classification |
|---|---|
| 🖐️ Open Palm | Open Palm |
| 👍 Thumbs Up | Thumbs Up |
| 👎 Thumbs Down | Thumbs Down |
| ☝️ Pointing | Pointing |
| ✌️ Victory | Victory |
| ✊ Fist | Fist |

The trained models are stored in the `models` directory and loaded during real-time inference.

## 4. Confidence-Based Prediction

A confidence threshold is used to reduce incorrect gesture predictions.

A gesture is accepted only when the model's prediction confidence reaches the configured threshold.

This prevents uncertain predictions from immediately triggering computer-control actions.

## 5. Gesture Smoothing

Real-time camera input can produce rapidly changing predictions.

A gesture smoothing mechanism uses recent predictions to stabilize the output and reduce unwanted switching between gesture classes.

This improves the reliability of real-time interaction.

---

# 🎮 Original Gesture-to-Action Mapping

The original gesture controller supports the following mappings:

| Gesture | Computer / Media Action |
|---|---|
| 🖐️ Open Palm | Play / Pause |
| 👍 Thumbs Up | Volume Up |
| 👎 Thumbs Down | Volume Down |
| ☝️ Pointing | Next Track |
| ✌️ Victory | Previous Track |
| ✊ Fist | Mute |

These actions are implemented through keyboard and media-control automation.

---

# 🎵 GestureMusic – Apple Music Integration

GestureMusic extends the original gesture recognition project by connecting the machine learning pipeline to a web-based interface and Apple Music on Windows.

Instead of relying only on direct computer-control actions, GestureMusic uses a FastAPI backend to process webcam frames and communicate gesture predictions to the frontend in real time.

### Key Features

- Real-time webcam input.
- MediaPipe-based hand landmark detection.
- Machine learning gesture classification.
- Confidence-based prediction.
- Gesture smoothing.
- FastAPI backend.
- WebSocket-based communication.
- Apple Music Windows media-key integration.
- Browser-based monitoring of detected gestures and confidence scores.

### GestureMusic Media Controls

| Gesture | Intended Action |
|---|---|
| 🖐️ Open Palm | Play / Pause |
| ☝️ Pointing | Next Track |
| ✌️ Victory | Previous Track |

**Current integration testing status:**

- Pointing → Next Track: Successfully tested.
- Open Palm → Play / Pause: Requires further validation.
- Victory → Previous Track: Requires further validation.

The original controller retains the additional volume and mute mappings. These are not yet integrated into the current Apple Music controller.

---

# 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Hand Detection | MediaPipe |
| Machine Learning | Scikit-learn |
| Data Processing | NumPy, Pandas |
| Automation | PyAutoGUI, Keyboard |
| Backend | FastAPI |
| Real-Time Communication | WebSockets |
| Frontend | HTML, CSS, JavaScript |
| Development Tools | VS Code, Git, GitHub |

---

# 📁 Project Structure

```text
AI_Hand_Gesture_Project/
│
├── app/
├── data/
│
├── Demo/
│   └── project_output_next_track.mp4
│
├── GestureMusic-starter/
│   └── GestureMusic/
│       │
│       ├── backend/
│       │   ├── app.py
│       │   └── requirements.txt
│       │
│       ├── frontend/
│       │   ├── index.html
│       │   ├── script.js
│       │   └── style.css
│       │
│       └── README.md
│
├── models/
│   ├── gesture_model.pkl
│   └── gesture_model_enhanced.pkl
│
├── notebooks/
│
├── src/
│   ├── camera.py
│   ├── collect_data.py
│   ├── feature_extractor.py
│   ├── gesture_controller.py
│   ├── gesture_smoother.py
│   ├── hand_detector.py
│   ├── realtime_gesture.py
│   ├── train_model.py
│   ├── apple_music_controller.py
│   └── test_apple_music.py
│
├── tests/
│   └── test_controller.py
│
├── execution.txt
├── hand_landmarker.task
├── .gitignore
└── README.md
```

---

# 🚀 Installation & Execution

## Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies.
- Webcam.
- Windows operating system for Apple Music media-key integration.
- Apple Music Windows application.
- Required trained model files.
- MediaPipe hand landmarker task file.

## 1. Clone the Repository

```bash
git clone https://github.com/Ashishsambari/AI_Hand_Gesture_Project.git
```

Navigate to the project directory:

```bash
cd AI_Hand_Gesture_Project
```

## 2. Set Up Python Environment

Create a virtual environment:

```bash
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies required by the original gesture recognition project and GestureMusic backend.

For the GestureMusic backend:

```bash
pip install -r GestureMusic-starter/GestureMusic/backend/requirements.txt
```

Ensure all original computer vision and machine learning dependencies are installed as well.

## 3. Start the GestureMusic Backend

Open a terminal in the main project directory and run:

```bash
python -m uvicorn app:app --app-dir "GestureMusic-starter/GestureMusic/backend" --reload --port 8000
```

Backend health endpoint:

```text
http://127.0.0.1:8000/api/health
```

## 4. Start the Frontend

Open a second terminal in the main project directory.

Run:

```bash
python -m http.server 5500 --directory "GestureMusic-starter/GestureMusic/frontend"
```

Open the application in your browser:

```text
http://localhost:5500
```

Keep both terminals running while using GestureMusic.

**Note:** The backend requires the trained model, MediaPipe task file, and compatible Python dependencies to be available at their expected project paths.

---

# 📊 Output

The original gesture recognition system displays real-time gesture predictions and confidence information.

Example:

```text
Detected Gesture : THUMBS UP
Confidence       : High
Action            : Volume Up
```

GestureMusic additionally displays gesture predictions through its browser-based interface.

Example:

```text
Detected Gesture : POINTING
Confidence       : High
Action            : Next Track
```

---

# 📈 Performance & Testing

The system was developed and tested with six predefined hand gesture classes.

The original pipeline includes:

- Real-time hand detection.
- Landmark-based feature extraction.
- Supervised machine learning classification.
- Confidence-based filtering.
- Gesture smoothing.
- Computer-control integration.

GestureMusic was tested for frontend/backend communication and real-time gesture prediction through WebSockets.

Pointing-based next-track media control was successfully tested.

Exact model test accuracy should be reported only when measured using an appropriate held-out test dataset.

---

# ⚠️ Limitations

The performance of the system can be affected by:

- Lighting conditions.
- Webcam quality.
- Hand position and distance.
- Finger occlusion.
- Background conditions.
- Similar-looking hand gestures.
- Model confidence and prediction stability.

GestureMusic currently has partially validated Apple Music media controls. Additional testing is required for reliable play/pause and previous-track functionality.

The Apple Music integration uses Windows media-key automation rather than a direct Apple Music API integration.

---

# 🔮 Future Improvements

- Improve gesture recognition accuracy and robustness.
- Add more gesture classes.
- Improve recognition under different lighting conditions.
- Support multiple hands.
- Add customizable gesture-to-action mappings.
- Complete and validate all Apple Music controls.
- Add volume and mute controls to GestureMusic.
- Improve WebSocket connection handling.
- Add user-configurable confidence thresholds.
- Develop a standalone desktop application.
- Explore edge-AI deployment.
- Add voice and gesture-based multimodal interaction.

---

# 🎯 Conclusion

This project demonstrates how computer vision and machine learning can be combined to build real-time human-computer interaction systems.

By integrating MediaPipe hand landmark detection, feature extraction, supervised machine learning, confidence-based prediction, and gesture smoothing, the system recognizes hand gestures and translates them into practical computer-control actions.

The GestureMusic extension further demonstrates the integration of an AI-powered gesture recognition pipeline with a web-based frontend, FastAPI backend, WebSocket communication, and Windows media controls.

The project provides practical experience across the complete AI/ML development lifecycle, from data collection and feature engineering to model training, real-time inference, backend integration, and application-level automation.

---

## 👨‍💻 Author

**Ashish Sambari**

B.Tech – Artificial Intelligence & Data Science

---

## ⭐ Project Repository

[AI Hand Gesture Recognition & GestureMusic – GitHub](https://github.com/Ashishsambari/AI_Hand_Gesture_Project)

If you find this project interesting, consider giving the repository a ⭐ on GitHub.
