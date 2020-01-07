from logutil import logger


def calculate_move_map(variables):
    width, height = variables.device_screen_width, variables.device_screen_height
    center_x, center_y = width / 2, height / 2  # 屏幕中心坐标
    horizontal_unit_distance = width / 3  # 水平方向每次移动距离
    vertical_unit_distance = height / 3  # 垂直方向每次移动距离
    if variables.swipe_mode == 0:
        logger.debug('↑')  # 手势从上往下，查看上侧区域
        to_x = center_x
        to_y = center_y + vertical_unit_distance
        variables.swipe_mode = 1  # 下次向右滑动
    elif variables.swipe_mode == 1:
        logger.debug('→')  # 手势从右往左，查看右侧区域
        to_x = center_x - horizontal_unit_distance
        to_y = center_y
        variables.swipe_mode = 2  # 下次向下滑动
    elif variables.swipe_mode == 2:
        logger.debug('↓')  # 手势从下往上，查看下侧区域
        to_x = center_x
        to_y = center_y - vertical_unit_distance * 2
        variables.swipe_mode = 3  # 下次向左滑动
    else:
        logger.debug('←')  # 手势从左往右，查看左侧区域
        to_x = center_x + horizontal_unit_distance * 2
        to_y = center_y
        variables.swipe_mode = 0  # 下次向上滑动
    return center_x, center_y, to_x, to_y
