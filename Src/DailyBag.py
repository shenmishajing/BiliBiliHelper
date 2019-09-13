# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了每日礼包功能
# 代码根据metowolf大佬的PHP版本进行改写

import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from config import config
from Curl import Curl
from Base import std235959

class DailyBag():
    def __init__(self):
        self.lock_web = int(time.time())
        self.lock_mobile = int(time.time())

    def work(self):
        if config["Function"]["DAILYBAG"] == "False":
            return
        if self.lock_web < int(time.time()):
            self.web()
        if self.lock_mobile < int(time.time()):
            self.mobile()
        
    
    def web(self):
        url = "https://api.live.bilibili.com/gift/v2/live/receive_daily_bag"
        payload = {}
        data = Curl().request_json("GET",url,headers=config["pcheaders"],params=payload)
        
        if data["code"] != 0:
            Log.warning("每日礼包领取失败")
            self.lock_wb = int(time.time()) + 600
            return
        else:
            Log.info("每日礼包领取成功")
            self.lock_web = std235959() + 600
            return

    def mobile(self):
        url = "https://api.live.bilibili.com/AppBag/sendDaily"
        payload = {}
        data = Curl().request_json("GET",url,headers=config["pcheaders"],params=payload)
        
        if data["code"] != 0:
            Log.warning("每日礼包领取失败(APP)")
            self.lock_mobile = int(time.time()) + 600
            return
        else:
            Log.info("每日礼包领取成功(APP)")
            self.lock_mobile = std235959() + 600
            return

