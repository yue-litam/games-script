# coding: utf-8

import cv2
import numpy as np
from common.logutil import logger


def get_similarity(template, screen, threshold=0.8):
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    possible_targets = []
    w, h = template.shape[::-1]
    for possible_target in zip(*loc[::-1]):
        x, y = possible_target[0] + w / 2, possible_target[1] + h / 2
        if len(possible_targets) > 0:
            last = possible_targets[len(possible_targets) - 1]
            if x - last[0] > 30: # 误差在30内视为同一个区域
                possible_targets.append((x, y))
        else:
            possible_targets.append((x, y))
    logger.debug(possible_targets)
    return possible_targets


def device_detect_feature_location_handler(feature, screen):
    w, h = feature.shape[::-1]
    res = cv2.matchTemplate(screen, feature, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    touch_loc = (max_loc[0], max_loc[1])
    return touch_loc, max_loc, w, h


def find_click_position(template, screen, x_offset=0, y_offset=0):
    touch_loc, _, w, h = device_detect_feature_location_handler(template, screen)
    return (touch_loc[0] + w / 2 + x_offset), (touch_loc[1] + h / 2 + y_offset)


def load_resource(resource, prefix=""):
    return cv2.imread(prefix + resource, 0)
