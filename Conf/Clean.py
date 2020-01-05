# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 直接在git的项目改的,测试要要清理配置文件很烦。
# 干脆写一个小脚本,快速删除重要信息

import os
from configobj import ConfigObj

account = ConfigObj(os.getcwd()+"/Account.conf", encoding="UTF8")
config = ConfigObj(os.getcwd()+"/BiliBiliHelper.conf", encoding="UTF8")

account["Account"]["BILIBILI_USER"] = ""
account["Account"]["BILIBILI_PASSWORD"] = ""
account["Token"]["ACCESS_TOKEN"] = ""
account["Token"]["REFRESH_TOKEN"] = ""
account["Token"]["CSRF"] = ""
account["Token"]["UID"] = ""
account["Token"]["COOKIE"] = ""
config["Live"]["ROOM_ID"] = ""
config["pcheaders"]["cookie"] = ""
account.write()
config.write()