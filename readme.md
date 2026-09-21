# 🤖 AI Hand Gesture Recognition & Media Controller

A real-time AI-based hand gesture recognition system that uses computer vision and machine learning to recognize hand gestures through a webcam and convert them into computer/media control actions.

The project combines **hand landmark detection, feature extraction, machine learning classification, confidence-based prediction, and gesture smoothing** to provide stable real-time interaction.

---

## 📌 Project Overview

This project was developed to create a **touch-free human-computer interaction system** using hand gestures.

A webcam captures the user's hand movements, the hand is detected and converted into numerical landmark features, and a trained machine learning model predicts the corresponding gesture.

The predicted gesture is then mapped to a specific computer/media-control action.

### Workflow

```text
Webcam
   ↓
Hand Detection
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

---

# 🧠 Algorithms & Techniques Used

## 1. Hand Landmark Detection

The system uses **MediaPipe Hand Landmarker** to detect the hand and identify key landmark points.

The detected hand is represented using a set of landmark coordinates corresponding to different parts of the hand.

These landmarks provide the geometric information required for gesture recognition.

---

## 2. Feature Extraction

The detected hand landmarks are converted into numerical features that can be provided to the machine learning model.

Feature extraction transforms the visual hand information into a structured numerical representation.

This allows the machine learning model to classify different hand poses.

---

## 3. Machine Learning Classification

A supervised machine learning classification model is trained using the extracted hand landmark features.

The model learns the relationship between landmark features and predefined gesture classes.

### Gesture Classes

The project recognizes six gestures:

| Gesture        | Classification |
| -------------- | -------------- |
| 🖐️ Open Palm  | Open Palm      |
| 👍 Thumbs Up   | Thumbs Up      |
| 👎 Thumbs Down | Thumbs Down    |
| ☝️ Pointing    | Pointing       |
| ✌️ Victory     | Victory        |
| ✊ Fist         | Fist           |

The trained model is stored in the `models` directory and is used during real-time prediction.

---

## 4. Confidence-Based Prediction

The system uses a **confidence threshold** to reduce incorrect gesture predictions.

A gesture is accepted only when the model's prediction confidence reaches the required threshold.

This helps prevent unstable or uncertain predictions from triggering computer actions.

```text
Prediction
     ↓
Confidence Check
     ↓
 ┌───────────────┐
 │ High confidence│ → Accept gesture
 └───────────────┘

 ┌───────────────┐
 │ Low confidence │ → Ignore prediction
 └───────────────┘
```

---

## 5. Gesture Smoothing

Real-time camera input can produce rapidly changing predictions even when the user is holding the same gesture.

A **gesture smoothing mechanism** is implemented to stabilize predictions.

Instead of immediately responding to every individual frame, the system uses recent predictions to reduce unwanted switching between gestures.

This improves the reliability of the real-time controller.

---

# 🎮 Gesture-to-Action Mapping

Each recognized gesture is mapped to a computer/media-control action.

| Gesture        | Action       |
| -------------- | ------------ |
| 🖐️ Open Palm  | Play / Pause |
| 👍 Thumbs Up   | Volume Up    |
| 👎 Thumbs Down | Volume Down  |
| ☝️ Pointing    | Next         |
| ✌️ Victory     | Previous     |
| ✊ Fist         | Mute         |

The actions are performed using keyboard/media-control automation.

---

# 📊 Output

The final output of the system is a real-time gesture prediction displayed while the webcam is running.

For example:

```text
Detected Gesture : THUMBS UP
Confidence        : High
Action            : Volume Up
```

Similarly:

```text
Detected Gesture : OPEN PALM
Action            : Play / Pause
```

The system continuously processes the webcam input and responds to recognized gestures.

---

# 🖥️ Real-Time System Output

The application provides:

* Real-time hand detection
* Real-time gesture classification
* Gesture confidence evaluation
* Smoothed predictions
* Automatic computer/media control

The system can therefore be used as a **touch-free media controller**.

---

# 🛠️ Technologies Used

* **Python**
* **OpenCV**
* **MediaPipe**
* **NumPy**
* **Pandas**
* **Scikit-learn**
* **PyAutoGUI**
* **Keyboard automation**
* **Machine Learning**
* **Computer Vision**

---

# 📁 Project Structure

```text
AI_Hand_Gesture_Project/
│
├── data/
│   ├── Gesture datasets
│   └── Enhanced datasets
│
├── models/
│   └── Trained machine learning models
│
├── src/
│   ├── camera.py
│   ├── collect_data.py
│   ├── feature_extractor.py
│   ├── gesture_controller.py
│   ├── gesture_smoother.py
│   ├── hand_detector.py
│   ├── realtime_gesture.py
│   └── train_model.py
│
├── .gitignore
├── hand_landmarker.task
└── README.md
```

---

# 🔄 Machine Learning Pipeline

### Step 1 — Data Collection

Hand gesture samples are collected using the webcam.

### Step 2 — Hand Detection

The hand is detected using the hand landmark detection model.

### Step 3 — Feature Extraction

Landmark coordinates are converted into numerical features.

### Step 4 — Model Training

The extracted features are used to train a supervised machine learning classification model.

### Step 5 — Model Saving

The trained model is saved for real-time inference.

### Step 6 — Real-Time Prediction

The webcam continuously captures frames and the trained model predicts the current gesture.

### Step 7 — Confidence Filtering

Low-confidence predictions are ignored.

### Step 8 — Gesture Smoothing

Predictions are stabilized to prevent rapid unwanted gesture changes.

### Step 9 — Computer Control

The final gesture is converted into a predefined keyboard/media action.

---

# 📈 Performance

The system was tested with six different gesture classes:

* Open Palm
* Thumbs Up
* Thumbs Down
* Pointing
* Victory
* Fist

The model successfully recognizes the defined gestures and connects the predictions to real-time computer-control actions.

> **Note:** Add the exact test accuracy here if you have a measured test-set accuracy. Do not use training accuracy as test accuracy.

---

# ⚠️ Limitations

The performance of a vision-based gesture recognition system can be affected by:

* Lighting conditions
* Camera quality
* Hand position
* Distance from the camera
* Occlusion of fingers
* Similar-looking hand gestures
* Background conditions

---

# 🚀 Future Improvements

Possible improvements include:

* Add more gesture classes
* Improve recognition under different lighting conditions
* Support multiple hands
* Add customizable gesture-to-action mappings
* Improve robustness against background changes
* Deploy the system as an edge-AI application
* Add voice and gesture multimodal interaction
* Create a graphical user interface for configuration

---

# ✅ Conclusion

This project demonstrates how **computer vision and machine learning can be combined to create a real-time human-computer interaction system**.

By using hand landmark detection, feature extraction, supervised classification, confidence-based prediction, and gesture smoothing, the system can recognize predefined hand gestures and translate them into practical computer/media-control actions.

The project provides practical experience across the complete machine learning pipeline — from **data collection and feature engineering to model training, real-time inference, and application-level control**.

It can serve as a foundation for more advanced applications such as **touchless interfaces, accessibility systems, smart-device control, gaming interfaces, and edge-AI human-computer interaction**.

---

## 👨‍💻 Author

**Ashish Sambari**

B.Tech — Artificial Intelligence & Data Science

---

## ⭐ Project

If you found this project interesting, consider giving the repository a ⭐ on GitHub.
