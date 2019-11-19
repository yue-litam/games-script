# coding: utf-8

import cv2


class Scene:
    image_name = ''
    action = ''
    action_button_name = None

    # image_name : the image to scan to identify the scene
    # action : the action to execute upon match with image_name, receives (template, img), where
    #           template is the cv2 rep of the action_button_name below, and the image is the
    #           current screen shot
    # action_button_name: sometimes we want different button to be clicked while not checking this button
    #           the default value is the same as image_name
    def __init__(self, image_name, action, action_button_name=None, assets_path_prefix=''):
        if action_button_name is None:
            action_button_name = image_name
        self.image_name = image_name
        self.action = action
        self.action_button_name = action_button_name

        # load resources
        self.imageTemplate = cv2.imread(assets_path_prefix + image_name, 0)
        if self.imageTemplate is None:
            print("Error : ImageName is wrong")

        self.actionTemplate = cv2.imread(assets_path_prefix + action_button_name, 0)
        if self.actionTemplate is None:
            print("Error : ActionButtonName is wrong")

        print("scene register: <{0}> action: <{1}>".format(image_name, action_button_name))
