# coding: utf-8

import cv2
import numpy as np


def device_detect_feature_location_handler(feature, screen):
    w, h = feature.shape[::-1]
    res = cv2.matchTemplate(screen, feature, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    touch_loc = (max_loc[0], max_loc[1])
    return touch_loc, max_loc, w, h


def get_similarity(template, img, scene=None, threshold=0.8):
    _, _ = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    found = 0
    for _ in zip(*loc[::-1]):
        found = 1
        break
    return found
