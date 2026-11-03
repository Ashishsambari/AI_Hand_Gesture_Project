import pyautogui
import time

print("Start a song in Apple Music.")
input("Press Enter when ready...")

print("Pausing...")
pyautogui.press("playpause")
time.sleep(3)

print("Resuming...")
pyautogui.press("playpause")
time.sleep(3)

print("Going to previous track...")
pyautogui.press("prevtrack")
time.sleep(2)
pyautogui.press("prevtrack")

print("Test completed!")