# coding: utf-8

# In[6]:


import wda
import cv2
import time
import sys
import numpy as np

# In[6]:


deviceVersion = 'iphone_se_3.0.0/feature/'
threshold = 0.8  # 近似度阈值

# targetLevel = '3_1'
if len(sys.argv) <= 1:
    defaultLevel = '3_1'
else:
    defaultLevel = sys.argv[1]
targetLevel = defaultLevel
print("execute level is", targetLevel)

# In[7]:


# 连接iOS设备，请在此处替换为你的iOS启动的WDA Test的ip地址
# c = wda.Client('http://192.168.3.52:8100')

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
    # if spec is not None:
    #     print('check if is', spec.image_name)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    loc = np.where(res >= threshold)
    found = 0
    for pt in zip(*loc[::-1]):
        found = 1
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
    # pick the highest applicable key
    # ss = max(specs, key=lambda s: get_similarity(s.imageTemplate, img, s))
    ss = None
    for spec in specs:
        match = get_similarity(spec.imageTemplate, img, spec) == 1
        if match:
            ss = spec
            break
    if ss is None:
        print('unable recognize stage, wait for next time.')
        return

    # perform second filtering to filter by the actionButtonTemplate
    spec_name = ss.image_name
    filtered = [s for s in specs if s.image_name == ss.image_name]
    print("= = = = = = = = = = = = = =")

    # ss = max(filtered, key=lambda s: get_similarity(s.actionTemplate, img, s))
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


# In[16]:


def login_screen_spec():
    def f(template, img):
        touch_button(template, img, 200)

    return Spec("login_server_selection.png", f)


# In[17]:


def close_event_screen_spec():
    return Spec("event_overview.png", touch_button, "event_overview_close.png")


# In[18]:


def close_announcement_screen_spec():
    return Spec("system_announcement.png", touch_button, "cross_close_button.png")


# In[19]:


def start_battle_from_home_screen_spec():
    return Spec("start_battle_home_screen.png", touch_button)


# In[20]:


def choose_battle_level_spec():
    return Spec("battle_" + targetLevel + '.png', touch_button)


# In[21]:


def choose_battle_level_confirm_spec():
    return Spec("choose_level_go_now_button.png", touch_button)


# In[24]:


def map_move_spec_question_mark():
    def f(template, img):
        touch_button(template, img, 0, 50)

    return Spec("explore_map_question_mark.png", f, "explore_map_question_mark.png")


# In[25]:


def map_move_spec_boss():
    return Spec("boss_icon_detection.png", touch_button, "boss_icon_detection.png")


# In[26]:


def map_move_spec_ship1():
    return Spec("map_ship_type_1.png", touch_button)


def map_move_spec_ship2():
    return Spec("map_ship_type_2.png", touch_button)


def map_move_spec_ship3():
    return Spec("map_ship_type_3.png", touch_button)


def map_move_spec_ship4():
    return Spec("map_ship_type_4.png", touch_button)


# In[29]:


def map_move_ambush_encountered():
    return Spec("ambush_encountered_detection.png", touch_button, "map_move_evade_ambush.png")


# In[30]:


def map_battle_preview_spec():
    return Spec("battle_prepare.png", touch_button, "battle_preview_start_button.png")


# In[31]:


def battle_start_auto_fight_spec():
    return Spec("not_auto_fighting_detection.png", touch_button)


# In[32]:


def battle_start_auto_fight_confirmation_spec():
    return Spec("auto_battle_warning_detection.png", touch_button, "auto_battle_confirm_button.png")


# In[33]:


def battle_in_good_state():
    def f(template, img):
        print('waiting for battle to finish.')
        pass

    return Spec("stop_auto_battle_detection.png", f)


# In[34]:


def battle_post_continue_spec():
    return Spec("battle_post_view_s_level.png", touch_button)


def battle_post_items_drop_spec():
    return Spec("battle_post_view_get_items_detection.png", touch_button)


def battle_post_exp_spec():
    return Spec("battle_post_confirm_detection.png", touch_button, "battle_post_confirm_button.png")


# In[37]:


def battle_post_view_new_character_confirmation():
    def f(template, img):
        touch_button(template, img, 0, 200)

    return Spec("battle_post_new_character_detection.png", f)


# In[38]:


def battle_post_view_new_character_lock_confirmation():
    return Spec("whether_locking_this_ship_detection.png", touch_button, "ship_lock_yes_button.png")


# In[39]:


def dismiss_info_box_spec():
    return Spec("info_box_detection.png", touch_button, "cross_close_button.png")


# In[41]:


specs = [
    login_screen_spec,  # 登陆界面
    close_announcement_screen_spec,  # 关闭公告界面
    close_event_screen_spec,  # 关闭活动总览界面
    start_battle_from_home_screen_spec,  # 从主界面进入战斗界面
    choose_battle_level_spec,  # 选择战斗关卡（请在顶部配置变量targetLevel，如3_4）
    choose_battle_level_confirm_spec,  # 战斗关卡确认出击按钮（包括下一界面的队伍选择确认出击）
    map_battle_preview_spec,  # 战斗前队伍预览
    battle_start_auto_fight_spec,  # 未开启自律模式
    battle_start_auto_fight_confirmation_spec,  # 开启自律模式的警告
    battle_post_view_new_character_confirmation,  # 战斗结束后获得新/四星/五星角色确认
    battle_post_view_new_character_lock_confirmation,  # 战斗结束后获得新角色锁定确认
    map_move_ambush_encountered,  # 判断伏击舰队
    map_move_spec_boss,   # 判断boss舰队
    map_move_spec_ship4,  # 判断运输舰队
    map_move_spec_ship1,  # 判断侦查舰队
    map_move_spec_ship2,  # 判断航母舰队
    map_move_spec_ship3,  # 判断主力舰队
    map_move_spec_question_mark,  # 判断未知点
    battle_post_continue_spec,  # 战斗结束后判断获胜级别（S胜）
    battle_post_items_drop_spec,  # 战斗结束后获得物资
    battle_post_exp_spec,  # 战斗结束后获得经验
    battle_in_good_state,  # 自律战斗被关闭，当匹配到该图像时停止自动点击
    dismiss_info_box_spec  # 关闭信息（新的委托之类的）对话框
]
specs = [s() for s in specs]
while True:
    recognize_and_process_page(specs)
    time.sleep(1)
