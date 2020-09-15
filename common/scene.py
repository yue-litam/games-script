# coding: utf-8
from common import tool
from common.logutil import logger


class Scene:
    name = ''              # 场景名称
    identify_image = None  #
    type = 'tap'
    tap_offset_x = 0       # 该场景点击屏幕时在X轴方向偏移
    tap_offset_y = 0       # 该场景点击屏幕时在Y轴方向偏移
    tap_image = None       # 该场景点击位置的特征照片
    threshold = 0.8        # 匹配度，默认80%，可根据不同的素材调整

    def __init__(self, name, identify_image, action_type="tap",
                 tap_image=None, tap_offset_x=0, tap_offset_y=0,
                 threshold=0.8
                 ):
        self.name = name
        self.identify_image = identify_image
        self.type = action_type
        self.tap_image = tap_image
        self.tap_offset_x = tap_offset_x
        self.tap_offset_y = tap_offset_y
        self.threshold = threshold
        logger.debug("scene register: <{0}>".format(self.name))
        self.__check()

    def matched_in(self, screen):
        return tool.get_similarity(self.identify_image, screen, self.threshold)

    def how_to_swipe(self):
        raise NotImplemented('Scene Unknown how to swipe.')

    def where_to_tap(self, screen):
        x, y = tool.find_click_position(self.tap_image, screen)
        x += self.tap_offset_x
        y += self.tap_offset_y
        return x, y

    def perform_what(self):
        return self.type

    def __check(self):
        if self.identify_image is None:
            logger.error("Error : {0} Identify Image not exists".format(self.name))
            exit(0)
        if self.tap_image is None:
            self.tap_image = self.identify_image

    def before_action(self, device, screen):
        pass

    def after_action(self, device, screen):
        pass
