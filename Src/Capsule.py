# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 该代码实现了自动扭蛋功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/Capsule.php

import asyncio
import platform

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from Base import std235959ptm
from Config import *
from GuardRaffle import GuardRaffle


class Capsule:

    async def work(self):
        if config["Function"]["CAPSULE"] == "False":
            return

        while 1:
            sleep_time = GuardRaffle().get_sleep_time()
            if not sleep_time:
                count = await self.info()
                while count > 0:
                    if count >= 100:
                        status = await self.open(100)
                    elif count >= 10:
                        status = await self.open(10)
                    elif count > 0:
                        status = await self.open(1)
                    if not status:
                        await asyncio.sleep(6)
                        break
                    else:
                        count = await self.info()
                        await asyncio.sleep(3)
                if not count:
                    await asyncio.sleep(std235959ptm())
            else:
                Log.info("扭蛋模块退出活动，睡眠 {} s".format(sleep_time))
                await asyncio.sleep(sleep_time)

    async def info(self):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/get_detail"
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])

        if data["code"] != 0:
            Log.warning("扭蛋币余额查询异常")
            return 0

        Log.info("当前还有 %s 枚扭蛋币" % data["data"]["normal"]["coin"])

        return data["data"]["normal"]["coin"]

    async def open(self, num):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/open_capsule"
        csrf = account["Token"]["CSRF"]

        payload = {
            "type": "normal",
            "count": num,
            "csrf_token": csrf,
            "csrf": csrf
        }
        data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

        if data["code"] != 0:
            Log.warning("扭蛋失败,请稍后重试")
            return 0

        awards = data["data"]["awards"][0]
        if len(awards) != 0:
            Log.info("扭蛋成功,获得 %s 个 %s" % (awards["num"], awards["name"]))

        return num
