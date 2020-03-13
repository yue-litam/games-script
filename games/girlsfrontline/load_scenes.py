from common.logutil import logger
from common.scene import Scene
from common.tool import load_resource


def collect_friends_batteries(prefix):
    return Scene('获取好友电池',
                 identify_image=load_resource('collect_friend_batteries.png', prefix),
                 threshold=0.6)


def like_friend_dormitory(prefix):
    scene = Scene('给好友宿舍点赞',
                  identify_image=load_resource('like_friend_dormitory_button.png', prefix))
    return scene


def next_friend_dormitory(prefix, config, context):
    image = load_resource('next_friend_dormitory_button.png', prefix)
    width, _ = image.shape[::-1]

    def before_action(_1, _2):
        if context.like_friend_dormitory_count >= config.max_like_dormitory:
            logger.info('点赞数达成')
            exit(0)
        context.like_friend_dormitory_count += 1

    scene = Scene('前往下一位好友的宿舍', identify_image=image, tap_offset_x=width / 2 - 30)
    scene.before_action = before_action
    return scene


def load_scenes(prefix, config, context):
    prefix += "scenes_feature/"
    return [
        collect_friends_batteries(prefix),
        like_friend_dormitory(prefix),
        next_friend_dormitory(prefix, config, context)
    ]
