from gesture_controller import execute_action
import time


print("====================================")
print("     GESTURE CONTROLLER TEST")
print("====================================")
print()

print("Testing Open Palm...")
execute_action("open_palm")

time.sleep(2)

print("Testing Thumbs Up...")
execute_action("thumbs_up")

time.sleep(2)

print("Testing Thumbs Down...")
execute_action("thumbs_down")

time.sleep(2)

print("Testing Pointing...")
execute_action("pointing")

time.sleep(2)

print("Testing Victory...")
execute_action("victory")

time.sleep(2)

print("Testing Fist...")
execute_action("fist")

print()
print("Controller test completed!")