import logging
import pickle
from typing import Set

import cv2
import mediapipe as mp
import numpy as np

logger = logging.getLogger(__name__)


REQUIRED_HAND_COUNT = 2

hands = mp.solutions.hands.Hands()


class InvalidVideoFile(Exception):
    pass


class ModelClass:
    OK = 0
    NOT_OK = 1


with open('model.pickle', 'rb') as model_file:
    model = pickle.load(model_file)


def is_marked(multi_hand_landmarks) -> bool:
    for hand_landmarks in multi_hand_landmarks:
        hand_landmarks = [(landmark.x, landmark.y, landmark.z)
                          for landmark in hand_landmarks.landmark]
        flattened_landmarks = np.array(hand_landmarks).flatten()
        if model.predict([flattened_landmarks]) == ModelClass.NOT_OK:
            return False
    return True


def filter_sequential_marks(marks: Set[int]) -> Set[int]:
    off_from_last_mark = 0
    last_mark = None
    unique_marks = set()

    for mark in marks:
        if mark - off_from_last_mark != last_mark:
            last_mark = mark
            unique_marks.add(mark)
            off_from_last_mark = 1
        else:
            off_from_last_mark += 1

    return unique_marks


def get_marks(video_path: str) -> Set[int]:
    marked_vid_pos = set()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        logger.error('Failed to open video file %s', video_path)
        raise InvalidVideoFile

    logger.info('Processing video file %s', video_path)
    while True:
        _, frame = cap.read()

        if frame is None:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == REQUIRED_HAND_COUNT:
            if is_marked(result.multi_hand_landmarks):
                vid_pos = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                marked_vid_pos.add(vid_pos)

    cap.release()
    cv2.destroyAllWindows()

    marked_vid_pos = filter_sequential_marks(marked_vid_pos)
    logger.info('Video marks: %s', marked_vid_pos)
    return marked_vid_pos
