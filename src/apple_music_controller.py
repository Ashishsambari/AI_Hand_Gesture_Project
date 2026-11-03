
import pyautogui
import time

_last_action = None
_last_action_time = 0

ACTION_COOLDOWN = 1.5

GESTURE_ACTIONS = {
    "open_palm": "playpause",
    "pointing": "nexttrack",
    "victory": "prevtrack",
}

def execute_music_action(gesture):
    global _last_action, _last_action_time

    key = GESTURE_ACTIONS.get(gesture)

    if key is None:
        return

    now = time.time()

    # Avoid repeating the same command continuously.
    if gesture == _last_action and now - _last_action_time < ACTION_COOLDOWN:
        return

    pyautogui.press(key)

    _last_action = gesture
    _last_action_time = now

    print(f"GestureMusic: {gesture} -> {key}")
