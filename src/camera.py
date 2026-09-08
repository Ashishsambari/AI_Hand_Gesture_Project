import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Could not access the camera.")
        break

    # Display the camera feed
    cv2.imshow("Camera Test", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()