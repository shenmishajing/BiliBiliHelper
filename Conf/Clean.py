# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 直接在git的项目改的,测试要要清理配置文件很烦。
# 干脆写一个小脚本,快速删除重要信息

import sys
import optparse
from configobj import ConfigObj

parser = optparse.OptionParser()
parser.add_option("-t", "--token-only", action = "store_true", dest = "clean_token", help = "Clean Token Only")
(options, args) = parser.parse_args()

account = ConfigObj(sys.path[0] + "/Account.conf", encoding = "UTF8")
config = ConfigObj(sys.path[0] + "/BiliBiliHelper.conf", encoding = "UTF8")

if not options.clean_token:
    account["Account"]["BILIBILI_USER"] = ""
    account["Account"]["BILIBILI_PASSWORD"] = ""
    config["Live"]["ROOM_ID"] = ""
account["Token"]["ACCESS_TOKEN"] = ""
account["Token"]["REFRESH_TOKEN"] = ""
account["Token"]["CSRF"] = ""
account["Token"]["UID"] = ""
account["Token"]["COOKIE"] = ""
config["pcheaders"]["cookie"] = ""
account.write()
config.write()
