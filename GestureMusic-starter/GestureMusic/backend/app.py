
import os
import sys
import time

import cv2
import joblib
import mediapipe as mp
import numpy as np

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Locate the original AI project.
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

SRC_DIR = os.path.join(PROJECT_ROOT, "src")
MODEL_PATH = os.path.join(
    PROJECT_ROOT, "models", "gesture_model_enhanced.pkl"
)
HAND_MODEL_PATH = os.path.join(
    PROJECT_ROOT, "hand_landmarker.task"
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from feature_extractor import extract_landmarks
from apple_music_controller import execute_music_action
from gesture_smoother import GestureSmoother

app = FastAPI(title="GestureMusic API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIDENCE_THRESHOLD = 0.80


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_exists": os.path.isfile(MODEL_PATH),
        "hand_model_exists": os.path.isfile(HAND_MODEL_PATH),
    }


@app.websocket("/ws/gestures")
async def gesture_stream(websocket: WebSocket):
    await websocket.accept()

    detector = None

    try:
        if not os.path.isfile(MODEL_PATH):
            await websocket.send_json({
                "error": "Trained gesture model not found",
                "path": MODEL_PATH,
            })
            await websocket.close()
            return

        if not os.path.isfile(HAND_MODEL_PATH):
            await websocket.send_json({
                "error": "MediaPipe hand model not found",
                "path": HAND_MODEL_PATH,
            })
            await websocket.close()
            return

        model = joblib.load(MODEL_PATH)
        smoother = GestureSmoother(window_size=7)

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=HAND_MODEL_PATH
            ),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        detector = vision.HandLandmarker.create_from_options(options)

        last_timestamp = 0

        while True:
            message = await websocket.receive_json()

            if message.get("type") == "reset":
                smoother = GestureSmoother(window_size=7)
                await websocket.send_json({
                    "gesture": "waiting",
                    "confidence": 0.0,
                })
                continue

            image_data = message.get("image")
            if not image_data:
                continue

            import base64

            try:
                raw = base64.b64decode(image_data)
                frame = cv2.imdecode(
                    np.frombuffer(raw, dtype=np.uint8),
                    cv2.IMREAD_COLOR,
                )
                if frame is None:
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb,
                )

                last_timestamp = max(
                    last_timestamp + 1,
                    int(time.monotonic() * 1000),
                )
                results = detector.detect_for_video(
                    mp_image, last_timestamp
                )

                if not results.hand_landmarks:
                    await websocket.send_json({
                        "gesture": "no_hand",
                        "confidence": 0.0,
                    })
                    continue

                features = extract_landmarks(
                    results.hand_landmarks[0]
                )
                features_array = np.asarray(
                    features, dtype=np.float64
                ).reshape(1, -1)

                prediction = model.predict(features_array)[0]
                probabilities = model.predict_proba(
                    features_array
                )[0]
                confidence = float(np.max(probabilities))

                
                if confidence >= CONFIDENCE_THRESHOLD:
                    stable = smoother.update(str(prediction))
                    gesture = str(stable)

                    if stable is not None:
                        execute_music_action(gesture)
                else:
                    gesture = "uncertain"


                await websocket.send_json({
                    "gesture": gesture,
                    "confidence": round(confidence, 4),
                })

            except (ValueError, TypeError) as error:
                await websocket.send_json({
                    "error": f"Could not process camera frame: {error}"
                })

    except WebSocketDisconnect:
        pass
    finally:
        if detector is not None:
            detector.close()
