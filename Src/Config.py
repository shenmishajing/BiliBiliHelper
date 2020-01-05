# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel

import os
from configobj import ConfigObj

account = ConfigObj(os.getcwd()+"/Conf/Account.conf", encoding="UTF8")
config = ConfigObj(os.getcwd()+"/Conf/BiliBiliHelper.conf", encoding="UTF8")
