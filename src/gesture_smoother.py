from collections import deque, Counter


class GestureSmoother:

    def __init__(self, window_size=7):
        self.predictions = deque(maxlen=window_size)

    def update(self, gesture):

        self.predictions.append(gesture)

        # Wait until we have enough predictions
        if len(self.predictions) < 3:
            return gesture

        counts = Counter(self.predictions)

        stable_gesture, count = counts.most_common(1)[0]

        # Gesture is considered stable if it appears
        # at least 4 times in the recent predictions
        if count >= 4:
            return stable_gesture

        return gesture