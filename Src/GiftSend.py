# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 该代码实现了自动送出即将过期礼物的功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/GiftSend.php

import time
import asyncio
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from Config import *

class GiftSend:
    
    def __init__(self):
        self.uid = 0
        self.ruid = 0
        self.roomid = 0

    async def work(self):
        if config["Function"]["GIFTSEND"] == "False":
            return

        while 1:
            if self.ruid == 0:
                status = await self.getRoomInfo()
                if not status:
                    return

        
            url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
            data = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        
            if data["code"] != 0:
                Log.warning("背包查看失败!"+data["message"])
        
            if len(data["data"]["list"]) != 0:
                for each in data["data"]["list"]:
                    if each["expire_at"] >= data["data"]["time"] and each["expire_at"] <= data["data"]["time"] + int(config["GiftSend"]["TIME"]):
                        await self.send(each)
                        await asyncio.sleep(3)
                
            await asyncio.sleep(600)


    async def getRoomInfo(self):
        Log.info("正在生成直播间信息...")

        url = "https://api.bilibili.com/x/member/web/account"
        data = await AsyncioCurl().request_json("GET", url, headers=config["pcheaders"])

        if "code" in data and data["code"] != 0:
            Log.warning("获取账号信息失败!"+data["message"])
            Log.warning("清空礼物功能禁用!")
            return False
        
        self.uid = data["data"]["mid"]

        url = "https://api.live.bilibili.com/room/v1/Room/get_info"
        payload = {
            "id":config["Live"]["ROOM_ID"]
        }

        data = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"],params=payload)

        if data["code"] != 0:
            Log.warning("获取主播房间号失败!"+data["message"])
            Log.warning("清空礼物功能禁用!")
            return False

        Log.info("直播间信息生成完毕!")

        self.ruid = data["data"]["uid"]
        self.roomid = data["data"]["room_id"]

    async def send(self,value):
        url = "https://api.live.bilibili.com/gift/v2/live/bag_send"
        csrf = account["Token"]["CSRF"]
        
        payload = {
            "coin_type":"silver",
            "gift_id":value["gift_id"],
            "ruid":self.ruid,
            "uid":self.uid,
            "biz_id":self.roomid,
            "gift_num":value["gift_num"],
            "data_source_id":"",
            "data_behavior_id":"",
            "bag_id":value["bag_id"],
            "csrf_token":csrf,
            "csrf":csrf
        }
        data = await AsyncioCurl().request_json("POST", url, headers=config["pcheaders"], data=payload)
        
        if data["code"] != 0:
            Log.warning("送礼失败!"+data["message"])
        else:
            Log.info("成功向 %s 投喂了 %s 个 %s"%(payload["biz_id"],value["gift_num"],value["gift_name"]))
