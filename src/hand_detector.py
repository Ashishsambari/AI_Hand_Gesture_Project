import cv2
import mediapipe as mp
import os

from feature_extractor import extract_landmarks

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Find the model file
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "hand_landmarker.task"
)

print("Model path:", MODEL_PATH)
print("Model exists:", os.path.exists(MODEL_PATH))


# Create MediaPipe hand detector
base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)


# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

print("Camera started successfully.")
print("Show your hand clearly to the camera.")
print("Press Q to quit.")


timestamp_ms = 0


while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Create MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Timestamp must increase
    timestamp_ms += 33

    # Detect hands
    results = detector.detect_for_video(
        mp_image,
        timestamp_ms
    )

    # Number of detected hands
    hand_count = len(results.hand_landmarks)

    # Display detection status
    cv2.putText(
        frame,
        f"Hands detected: {hand_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Draw landmarks
    if hand_count > 0:

        for hand_landmarks in results.hand_landmarks:

            features = extract_landmarks(hand_landmarks)

            print("Number of features:", len(features))

            for landmark in hand_landmarks:

                height, width, _ = frame.shape

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    7,
                    (0, 255, 0),
                    -1
                )

    # Show camera
    cv2.imshow(
        "AI Hand Detection",
        frame
    )

    # Quit with Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()