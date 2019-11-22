# coding: utf-8

import cv2
import numpy as np


def get_similarity(template, screen, threshold=0.8):
    # _, _ = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    found = 0
    for _ in zip(*loc[::-1]):
        found = 1
        break
    return found


def device_detect_feature_location_handler(feature, screen):
    w, h = feature.shape[::-1]
    res = cv2.matchTemplate(screen, feature, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    touch_loc = (max_loc[0], max_loc[1])
    return touch_loc, max_loc, w, h


def find_click_position(template, screen, x_offset=0, y_offset=0):
    touch_loc, _, w, h = device_detect_feature_location_handler(template, screen)
    return (touch_loc[0] + w / 2 + x_offset), (touch_loc[1] + h / 2 + y_offset)
