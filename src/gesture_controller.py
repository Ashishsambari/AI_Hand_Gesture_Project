import pyautogui
import time


# Prevent accidental repeated actions
COOLDOWN = 1.0

last_gesture = None
last_action_time = 0


def execute_action(gesture):

    global last_gesture
    global last_action_time

    current_time = time.time()

    # Ignore if there is no valid gesture
    if gesture is None:
        return

    # Don't repeat the same gesture
    if gesture == last_gesture:
        return

    # Prevent actions happening too quickly
    if current_time - last_action_time < COOLDOWN:
        return

    # --------------------------------------------------
    # GESTURE ACTIONS
    # --------------------------------------------------

    if gesture == "open_palm":

        pyautogui.press("space")
        print("ACTION → PLAY / PAUSE")

    elif gesture == "thumbs_up":

        pyautogui.press("volumeup")
        print("ACTION → VOLUME UP")

    elif gesture == "thumbs_down":

        pyautogui.press("volumedown")
        print("ACTION → VOLUME DOWN")

    elif gesture == "pointing":

        pyautogui.press("right")
        print("ACTION → NEXT")

    elif gesture == "victory":

        pyautogui.press("left")
        print("ACTION → PREVIOUS")

    elif gesture == "fist":

        pyautogui.press("m")
        print("ACTION → MUTE")

    else:
        return

    # Remember the gesture that triggered the action
    last_gesture = gesture
    last_action_time = current_time


def reset_gesture():

    global last_gesture

    last_gesture = None