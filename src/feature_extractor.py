def extract_landmarks(hand_landmarks):
    """
    Convert 21 hand landmarks into
    63 wrist-relative features.
    """

    features = []

    # Wrist landmark
    wrist_x = hand_landmarks[0].x
    wrist_y = hand_landmarks[0].y
    wrist_z = hand_landmarks[0].z

    for landmark in hand_landmarks:

        x = landmark.x - wrist_x
        y = landmark.y - wrist_y
        z = landmark.z - wrist_z

        features.extend([
            x,
            y,
            z
        ])

    return features