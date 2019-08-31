# coding: utf-8

# In[6]:


import wda
import cv2
import time
import numpy as np

# In[6]:


deviceVersion = 'iphone_se_0.7.52/feature/'
threshold = 0.8  # 近似度阈值

# In[7]:


# 如果使用了WDA安装过程中提到的"libimobiledevice"进行端口转发，则替换为http://localhost:8100
c = wda.Client()
# print(c.status())
s = c.session()

# In[8]:


# 获取一张当前手机的截图
_ = c.screenshot('screen.png')

# In[9]:


# get some global properties
# 获取一些全局的数据，包括屏幕的宽高值，并输出到终端上
globalScreen = cv2.imread("screen.png", 0)
screenWidth, screenHeight = globalScreen.shape[::-1]
print("ScreenWidth: {0}, ScreenHeight: {1}".format(screenWidth, screenHeight))


# In[10]:


# 提供一个图片片段和一个完整的设备截屏图片对象，通过opencv在后者查找前者（片段）是否存在，并返回匹配率
# 匹配率会在终端打印出来
def get_similarity(template, img, spec=None):
    _, _ = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    found = 0
    for pt in zip(*loc[::-1]):
        found = 1
        break
    return found


# In[11]:


# 获取一张屏幕截图，并保存为temp.png
def take_screenshot():
    _ = c.screenshot('screen.png')
    img = cv2.imread('screen.png', 0)
    return img


# In[12]:


# get the location of template on image
# 返回图片片段在给定图片中的相对位置、片段的宽高
# @param img      给定图片，设备截屏
# @param template 图片片段
def get_button_location(template, img):
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    touch_loc = (max_loc[0], max_loc[1])
    return touch_loc, max_loc, w, h


# In[13]:


# touch the template on the image with offsets
# 模拟点击指定的按钮，如有必要，可通过参数三、四指定偏移
def touch_button(template, img, x_offset=0, y_offset=0):
    touch_loc, _, w, h = get_button_location(template, img)
    t_x, t_y = ((touch_loc[0] + w / 2 + x_offset) / 2, (touch_loc[1] + h / 2 + y_offset) / 2)
    print("Touching {0}, {1}".format(t_x, t_y))
    s.tap(t_x, t_y)


# In[14]:


def recognize_and_process_page(specs):  # in the form of image_name => (template, action)
    img = take_screenshot()
    print("===========================")
    ss = None
    for spec in specs:
        match = get_similarity(spec.imageTemplate, img, spec) == 1
        if match:
            ss = spec
            break
    if ss is None:
        print('unable recognize stage, wait for next time.')
        return

    spec_name = ss.image_name
    filtered = [s for s in specs if s.image_name == ss.image_name]
    print("= = = = = = = = = = = = = =")

    ss = None
    for spec in filtered:
        match = get_similarity(spec.actionTemplate, img, spec) == 1
        if match:
            ss = spec
            break
    if ss is None:
        print('stage', spec_name, 'unable recognize action feature, program would not tap any position.')
    else:
        print("Picked : " + ss.image_name + " ==> " + ss.action_button_name)
        ss.action(ss.actionTemplate, img)


# In[15]:


class Spec:
    # image_name : the image to scan to identify the scene
    # action : the action to execute upon match with image_name, receives (template, img), where
    #           template is the cv2 rep of the action_button_name below, and the image is the
    #           current screen shot
    # action_button_name: sometimes we want different button to be clicked while not checking this button
    #           the default value is the same as image_name
    def __init__(self, image_name, action, action_button_name=None):
        if action_button_name is None:
            action_button_name = image_name
        self.image_name = image_name
        self.action = action  # action must receive (template, img) as the input variable
        self.action_button_name = action_button_name

        # load resources
        self.imageTemplate = cv2.imread(deviceVersion + image_name, 0)
        if self.imageTemplate is None:
            print("Error : ImageName is wrong")

        self.actionTemplate = cv2.imread(deviceVersion + action_button_name, 0)
        if self.actionTemplate is None:
            print("Error : ActionButtonName is wrong")

        print("\nProcessing Spec: \nImageName: {0}\nActionButtonName : {1}".format(
            image_name, action_button_name))
        # _ = cv2.imread(deviceVersion + image_name, 0)
        # _ = cv2.imread(deviceVersion + action_button_name, 0)


def confirm_battle_level_spec():
    def touch_offset(template, screen):
        w, h = template.shape[::-1]
        touch_button(template, screen, w)

    return Spec('level_info_detection.png', touch_offset)


def ptrs_disable_spec():
    return Spec('prts_disable_detection.png', touch_button)


def battle_team_preview_spec():
    return Spec('level_team_detection.png', touch_button)


def prts_running_spec():
    def touch_nothing(template, img):
        print('wait for fight finish.')
        pass

    return Spec('level_fighting_detection.png', touch_nothing)


def battle_post_upgrade_spec():
    return Spec('account_upgrade_detection.png', touch_button)


def battle_post_items_drop_spec():
    return Spec('level_finish_detection.png', touch_button)


def lack_of_mind_spec():
    def touch_nothing(template, img):
        print('mind used up, suspending scripts.')
        pass

    return Spec('lack_of_mind_detection.png', touch_nothing)


specs = [
    confirm_battle_level_spec,  # 战斗关卡确认出击
    ptrs_disable_spec,  # 战斗关卡确认出击
    battle_team_preview_spec,  # 战斗前队伍预览
    prts_running_spec,  # 战斗结束后账号等级提升
    battle_post_upgrade_spec,  # 战斗结束后账号等级提升
    battle_post_items_drop_spec,  # 战斗结束后账号等级提升
    lack_of_mind_spec,  # 战斗结束后账号等级提升
]
specs = [s() for s in specs]
while True:
    recognize_and_process_page(specs)
    time.sleep(1)
