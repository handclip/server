import logging
from dataclasses import dataclass
from enum import Enum
from typing import Set

import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

logger = logging.getLogger(__name__)


TIME_BETWEEN_GESTURES = 2

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.65)

model = load_model('mp_hand_gesture')


class HandGesture(Enum):
    OKAY = 0
    PEACE = 1
    THUMBS_UP = 2
    THUMBS_DOWN = 3
    CALL_ME = 4
    STOP = 5
    ROCK = 6
    LIVE_LONG = 7
    FIST = 8
    SMILE = 9


hand_gestures = {gesture.value: gesture for gesture in HandGesture}


@dataclass
class RecordedGesture:
    gesture: HandGesture = None
    video_position: int = None


def get_marks(video_path: str) -> Set[int]:
    cap = cv2.VideoCapture(video_path)
    last_gesture = None
    marks = set()

    while True:
        _, frame = cap.read()

        if frame is None:
            break

        x, y, _ = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(framergb)

        if result.multi_hand_landmarks:
            landmarks = []
            for hand_landmarks in result.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    landmarks.append([landmark.x * x, landmark.y * y])

                prediction = model.predict([landmarks])
                gesture = hand_gestures[np.argmax(prediction)]
                video_position = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)

                if last_gesture:
                    gestures_match = last_gesture.gesture == HandGesture.ROCK and gesture == HandGesture.FIST
                    video_position_match = last_gesture.video_position + TIME_BETWEEN_GESTURES >= video_position
                    if gestures_match and video_position_match:
                        marks.add(last_gesture.video_position)

                last_gesture = RecordedGesture(gesture, video_position)

    cap.release()
    cv2.destroyAllWindows()

    logger.info(f'Video marks: {marks}')
    return marks
