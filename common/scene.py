# coding: utf-8

import cv2


class Scene:
    name = ''  # 场景名称
    image = ''  # 场景特征照片
    before_action = None  # 前置处理函数
    action_tap = True  # 该场景是否需要点击屏幕
    action_tap_offset_x = 0  # 该场景点击屏幕时在X轴方向偏移
    action_tap_offset_y = 0  # 该场景点击屏幕时在Y轴方向偏移
    action_image = ''  # 该场景点击位置的特征照片
    after_action = None  # 后置处理函数
    action_swipe = False  # 该场景是否需要手势滑动
    action_handler = None  # 该场景手势滑动的处理器
    action_image_w = 0
    action_image_h = 0
    threshold = 0.8  # 匹配度，默认80%，可根据不同的素材调整

    def __init__(self,
                 image, prefix='', name=None,
                 before_action=None,
                 action_tap=True, action_image=None, action_tap_offset_x=0, action_tap_offset_y=0,
                 action_swipe=False, swipe_handler=None,
                 after_action=None,
                 threshold=0.8
                 ):

        self.image = image
        if name is None:
            self.name = image
        else:
            self.name = name
        if action_image is None:
            self.action_image = image
        else:
            self.action_image = action_image
        self.action_tap = action_tap
        self.before_action = before_action
        self.after_action = after_action
        self.action_swipe = action_swipe
        self.swipe_handler = swipe_handler
        self.action_tap_offset_x = action_tap_offset_x
        self.action_tap_offset_y = action_tap_offset_y
        self.threshold = threshold

        # load resources
        self.imageTemplate = cv2.imread(prefix + self.image, 0)
        if self.imageTemplate is None:
            print("Error : Image {0} not exists".format(self.image))
            exit(4)

        self.actionTemplate = cv2.imread(prefix + self.action_image, 0)
        if self.actionTemplate is None:
            print("Error : ActionImage {0} not exists".format(self.action_image))
            exit(4)
        self.action_image_w, self.action_image_h = self.actionTemplate.shape[::-1]

        print("scene register: <{0}> action: <{1}>".format(self.name, self.action_image))
