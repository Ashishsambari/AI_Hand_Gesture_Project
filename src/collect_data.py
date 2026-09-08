import cv2
import mediapipe as mp
import os
import csv
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from feature_extractor import extract_landmarks


# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "hand_landmarker.task"
)

DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "enhanced"
)

SAMPLES_PER_GESTURE = 800

# Time between saved samples
SAMPLE_INTERVAL = 0.08


# ============================================================
# GESTURES
# ============================================================

GESTURES = {
    ord("1"): "open_palm",
    ord("2"): "thumbs_up",
    ord("3"): "thumbs_down",
    ord("4"): "victory",
    ord("5"): "pointing",
    ord("6"): "fist"
}


# ============================================================
# CREATE DATA FOLDER
# ============================================================

os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)


# ============================================================
# CREATE MEDIAPIPE DETECTOR
# ============================================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(
    options
)


# ============================================================
# OPEN CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Could not open webcam.")
    exit()


print()
print("==============================================")
print("       ENHANCED GESTURE DATA COLLECTOR")
print("==============================================")
print()
print("1 = Open Palm")
print("2 = Thumbs Up")
print("3 = Thumbs Down")
print("4 = Victory")
print("5 = Pointing")
print("6 = Fist")
print()
print("Move your hand naturally while collecting.")
print()
print("Q = Quit")
print()


# ============================================================
# VARIABLES
# ============================================================

timestamp_ms = 0

last_sample_time = 0


# ============================================================
# MAIN CAMERA LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:

        print("Could not read camera.")
        break


    # Mirror camera
    frame = cv2.flip(
        frame,
        1
    )


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


    # Detect hand
    results = detector.detect_for_video(
        mp_image,
        timestamp_ms
    )


    # ========================================================
    # DRAW LANDMARKS
    # ========================================================

    if results.hand_landmarks:

        hand_landmarks = results.hand_landmarks[0]

        h, w, _ = frame.shape

        for landmark in hand_landmarks:

            x = int(
                landmark.x * w
            )

            y = int(
                landmark.y * h
            )

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )


    # ========================================================
    # DISPLAY INSTRUCTIONS
    # ========================================================

    cv2.putText(
        frame,
        "1-6: Select Gesture",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Q: Quit",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )    
    # ========================================================
    # SHOW CAMERA
    # ========================================================

    cv2.imshow(
        "Enhanced Data Collector",
        frame
    )


    # ========================================================
    # KEY INPUT
    # ========================================================

    key = cv2.waitKey(1) & 0xFF


    # Quit
    if key == ord("q"):

        break


    # ========================================================
    # GESTURE SELECTED
    # ========================================================

    if key in GESTURES:

        gesture_name = GESTURES[key]

        csv_path = os.path.join(
            DATA_FOLDER,
            f"{gesture_name}.csv"
        )


        print()
        print("==============================================")
        print(
            f"Selected gesture: {gesture_name}"
        )
        print("==============================================")
        print()
        print("Get ready...")
        print("Keep your hand visible.")
        print("Move your hand naturally.")
        print()


        # ----------------------------------------------------
        # 3 second countdown
        # ----------------------------------------------------

        for countdown in [3, 2, 1]:

            start_time = time.time()

            while time.time() - start_time < 1:

                ret, countdown_frame = cap.read()

                if not ret:
                    break

                countdown_frame = cv2.flip(
                    countdown_frame,
                    1
                )

                cv2.putText(
                    countdown_frame,
                    f"Starting in {countdown}",
                    (150, 250),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 255),
                    4
                )

                cv2.imshow(
                    "Enhanced Data Collector",
                    countdown_frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):

                    cap.release()
                    cv2.destroyAllWindows()
                    detector.close()
                    exit()


        # ----------------------------------------------------
        # Check existing samples
        # ----------------------------------------------------

        existing_samples = 0

        if os.path.exists(csv_path):

            with open(
                csv_path,
                "r",
                newline=""
            ) as file:

                existing_samples = sum(
                    1 for _ in file
                )


        print(
            f"Existing samples: {existing_samples}"
        )

        print(
            f"Collecting {SAMPLES_PER_GESTURE} "
            f"new samples..."
        )

        print()


        # ----------------------------------------------------
        # OPEN CSV
        # ----------------------------------------------------

        with open(
            csv_path,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            collected = 0

            last_sample_time = 0


            # =================================================
            # COLLECTION LOOP
            # =================================================

            while collected < SAMPLES_PER_GESTURE:

                ret, frame = cap.read()

                if not ret:
                    break


                frame = cv2.flip(
                    frame,
                    1
                )


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


                # ------------------------------------------------
                # Save only when hand detected
                # ------------------------------------------------

                if results.hand_landmarks:

                    current_time = time.time()


                    # Control sample frequency
                    if (
                        current_time -
                        last_sample_time
                        >= SAMPLE_INTERVAL
                    ):

                        hand_landmarks = (
                            results.hand_landmarks[0]
                        )


                        features = extract_landmarks(
                            hand_landmarks
                        )


                        writer.writerow(
                            features +
                            [gesture_name]
                        )


                        collected += 1

                        last_sample_time = (
                            current_time
                        )


                # ------------------------------------------------
                # DRAW LANDMARKS
                # ------------------------------------------------

                if results.hand_landmarks:

                    hand_landmarks = (
                        results.hand_landmarks[0]
                    )

                    h, w, _ = frame.shape

                    for landmark in hand_landmarks:

                        x = int(
                            landmark.x * w
                        )

                        y = int(
                            landmark.y * h
                        )

                        cv2.circle(
                            frame,
                            (x, y),
                            5,
                            (0, 255, 0),
                            -1
                        )


                # ------------------------------------------------
                # PROGRESS
                # ------------------------------------------------

                cv2.putText(
                    frame,
                    f"{gesture_name}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Samples: {collected}/{SAMPLES_PER_GESTURE}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "Move your hand naturally",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2
                )


                cv2.imshow(
                    "Enhanced Data Collector",
                    frame
                )


                # ESC = stop current collection
                if cv2.waitKey(1) & 0xFF == 27:

                    print(
                        "\nCollection interrupted."
                    )

                    break


        print()
        print(
            f"Finished collecting: "
            f"{gesture_name}"
        )

        print(
            f"Total samples in file: "
            f"{existing_samples + collected}"
        )

        print()


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

detector.close()

print()
print("Data collection stopped.")