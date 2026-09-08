import cv2
import mediapipe as mp
import os
import joblib
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from feature_extractor import extract_landmarks
from gesture_smoother import GestureSmoother
from gesture_controller import execute_action, reset_gesture


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "gesture_model_enhanced.pkl"
)

HAND_MODEL_PATH = os.path.join(
    BASE_DIR,
    "hand_landmarker.task"
)


# --------------------------------------------------
# LOAD GESTURE MODEL
# --------------------------------------------------

print("Loading gesture model...")

model = joblib.load(MODEL_PATH)

print("Gesture model loaded successfully!")


# --------------------------------------------------
# MEDIA PIPE HAND DETECTOR
# --------------------------------------------------

base_options = python.BaseOptions(
    model_asset_path=HAND_MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,

    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)


# --------------------------------------------------
# GESTURE SMOOTHER
# --------------------------------------------------

smoother = GestureSmoother(window_size=7)
CONFIDENCE_THRESHOLD = 0.80


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

print("Camera started successfully.")
print("Show your gestures.")
print("Press Q to quit.")


timestamp_ms = 0


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms += 33

    results = detector.detect_for_video(
        mp_image,
        timestamp_ms
    )


    # --------------------------------------------------
    # HAND DETECTED
    # --------------------------------------------------

    if results.hand_landmarks:

        hand_landmarks = results.hand_landmarks[0]

        # Extract 63 features
        features = extract_landmarks(
            hand_landmarks
        )

        features_array = np.array(
            features
        ).reshape(1, -1)


        # --------------------------------------------------
        # AI PREDICTION
        # --------------------------------------------------

        prediction = model.predict(
            features_array
        )[0]

        probabilities = model.predict_proba(
            features_array
        )[0]

        confidence = np.max(
            probabilities
        )


        # --------------------------------------------------
        # CONFIDENCE THRESHOLD
        # --------------------------------------------------

        if confidence >= CONFIDENCE_THRESHOLD:

            stable_prediction = smoother.update(
                prediction
            )

            # Send stable gesture to controller
            execute_action(stable_prediction)

        else:

            stable_prediction = "uncertain"

            # Allow the same gesture to trigger again
            # after the hand becomes uncertain
            reset_gesture()


        # --------------------------------------------------
        # DISPLAY
        # --------------------------------------------------

        if stable_prediction == "uncertain":
            gesture_text = "UNCERTAIN"
        else:
            gesture_text = stable_prediction.upper()

        confidence_text = (
            f"Confidence: {confidence * 100:.1f}%"
        )

        cv2.putText(
            frame,
            f"Gesture: {gesture_text}",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            confidence_text,
            (20, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # --------------------------------------------------
        # DRAW LANDMARKS
        # --------------------------------------------------

        height, width, _ = frame.shape

        for landmark in hand_landmarks:

            x = int(
                landmark.x * width
            )

            y = int(
                landmark.y * height
            )

            cv2.circle(
                frame,
                (x, y),
                6,
                (0, 255, 0),
                -1
            )


    # --------------------------------------------------
    # NO HAND
    # --------------------------------------------------

    else:

        cv2.putText(
            frame,
            "No hand detected",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )


    # --------------------------------------------------
    # SHOW CAMERA
    # --------------------------------------------------

    cv2.imshow(
        "AI Gesture Recognition",
        frame
    )


    # --------------------------------------------------
    # QUIT
    # --------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()
detector.close()

print("Program closed.")