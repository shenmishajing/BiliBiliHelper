# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel

import time
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log

class DailyBag():
    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["DAILYBAG"] == "False":
            return
        if self.lock > int(time.time()):
            return
    
    def web(self):
        url = "https://api.live.bilibili.com/gift/v2/live/receive_daily_bag"

        payload = {}

        data = Curl().request_json("POST",url,headers=config["pcheaders"],data=payload,sign=True)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning()
            return
        else:
            Log.info("")

    def mobile(self):
        url = "https://api.live.bilibili.com/AppBag/sendDaily"

        payload = {}
        
        data = Curl().grequest_json("POST",url,headers=config["pcheaders"],data=payload)
        data = json.load(data)

