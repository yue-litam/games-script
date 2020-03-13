import requests

from common.logutil import logger
from common.runtime import Config

url = "https://sc.ftqq.com/{0}.send?text={1}&desp={2}"
cfg = Config()


def program_exit_alert(cause):
    if cfg.server_chan_enable:
        secret = cfg.server_chan_secret
        params = {
            "title": "复读机复读结束通知",
            "desp": "游戏:{0}\n\n关卡:{1}\n\n结束原因:{2}\n\n" \
                .format(cfg.game_name, cfg.battle_no, cause)
        }
        resp = requests.get(url.format(secret, params['title'], params['desp']))
        json_string = bytes.decode(resp.content)
        logger.debug(json_string)
