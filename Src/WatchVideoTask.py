import asyncio
import platform
import random
import time
import math
import copy

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from Base import std235959ptm, std235959
from Config import *


class WatchVideoTask:
    instance = None

    # 单例模式
    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(WatchVideoTask, cls).__new__(cls, *args, **kw)
            cls.instance.need_vlist = {}
        return cls.instance

    async def get_need_vlist(self, Room_Id):
        if Room_Id in self.need_vlist:
            today = self.need_vlist[Room_Id]['today']
        else:
            today = None
        localtime = time.localtime(time.time())
        if today is None or localtime.tm_mday != today:
            Log.info(f"更新 up 主{Room_Id}的视频列表")
            need_vlist = []
            url = "https://api.bilibili.com/x/space/arc/search?ps=100&pn=1&mid=" + str(Room_Id)
            data = await AsyncioCurl().request_json("GET", url)
            pages = int(math.ceil(data["data"]["page"]["count"] / 100))
            for i in range(pages):
                url = f"https://api.bilibili.com/x/space/arc/search?ps=100&pn={i + 1}&mid={Room_Id}"
                data = await AsyncioCurl().request_json("GET", url)
                need_vlist.extend(data["data"]["list"]["vlist"])
            self.need_vlist[Room_Id] = {'need_vlist': need_vlist, 'today': localtime.tm_mday}
        else:
            Log.info(f"up 主{Room_Id}仍使用视频列表缓存")

    async def work(self):
        if config["Function"]["WatchVideoTask"] == "False":
            return

        Log.info("检查观看视频任务")

        # 必须有房间号才能运行
        if config["WatchVideoTask"]["ROOM_ID"] == "":
            Log.warning("观看视频模块up主号未配置,已停止...")
        else:
            sleep_time = random.randint(0, 15)
            Log.info('观看视频前，休眠 %d s，与其他观看任务错时启动' % sleep_time)
            await asyncio.sleep(sleep_time)
            await self.watch()

    async def watch(self):
        var = 0
        while True:
            var += 1
            if isinstance(config["WatchVideoTask"]["ROOM_ID"], list):
                Room_Id = random.choice(config["WatchVideoTask"]["ROOM_ID"])
            else:
                Room_Id = random.choice(config["WatchVideoTask"]["ROOM_ID"].split(","))
            Log.info("本次观看视频为第 %s 次，选择UP %s" % (var, Room_Id))
            await self.get_need_vlist(Room_Id)
            need_vilst = random.choice(self.need_vlist[Room_Id]['need_vlist'])

            Log.info("本次观看选择视频为标题  %s，BV： %s" % (need_vilst["title"], need_vilst["bvid"]))

            # 获取视频分P
            url = "https://api.bilibili.com/x/player/pagelist?bvid=" + need_vilst["bvid"]

            video_data = await AsyncioCurl().request_json("GET", url)

            for p in range(len(video_data["data"])):
                Log.info("正在观看 %s 第 %d p，共 %d p" % (need_vilst["bvid"], p + 1, len(video_data["data"])))
                video_cid = video_data["data"][p]["cid"]
                video_duration = video_data["data"][p]["duration"]

                url = "https://api.bilibili.com/x/click-interface/web/heartbeat"

                payload = {
                    'aid': need_vilst['aid'],
                    'cid': video_cid,
                    'bvid': need_vilst['bvid'],
                    'mid': need_vilst['mid'],
                    'csrf': account["Token"]["CSRF"],
                    'played_time': 0,
                    'real_played_time': 0,
                    'real_time': 0,
                    'start_ts': time.time(),
                    'type': 3,
                    'dt': 2,
                    'play_type': 0
                }

                headers = copy.deepcopy(config["pcheaders"])
                headers["Referer"] = "https://www.bilibili.com/%s" % need_vilst["bvid"]

                for i in range(video_duration // 15 + 1):
                    payload['played_time'] = payload['real_played_time'] = payload['real_time'] = i * 15
                    await AsyncioCurl().request_json("POST", url, headers = headers, data = payload)
                    if i < video_duration // 15:
                        await asyncio.sleep(15)
                    else:
                        await asyncio.sleep(video_duration - i * 15)
                        if i * 15 < video_duration:
                            payload['played_time'] = payload['real_played_time'] = payload['real_time'] = video_duration
                            await AsyncioCurl().request_json("POST", url, headers = headers, data = payload)

            # 看完了给点个赞
            url = "https://api.bilibili.com/x/web-interface/archive/like"
            payload = {
                "aid": need_vilst["aid"],
                "like": 1,
                "csrf": account["Token"]["CSRF"],
                "bvid": need_vilst["bvid"]
            }
            data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

            # if data["code"]:
            #     Log.error("出现错误 %s" % (data["message"]))

            # 分享一下
            url = "https://api.bilibili.com/x/web-interface/share/add"

            payload = {
                "aid": need_vilst["aid"],
                "jsonp": "jsonp",
                "csrf": account["Token"]["CSRF"]}

            data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

            if data["code"]:
                Log.error("出现错误 %s" % (data["message"]))

            # 再收藏一下
            url = "https://api.bilibili.com/medialist/gateway/coll/resource/deal"
            payload = {
                "rid": need_vilst["aid"],
                "type": 2,
                "csrf": account["Token"]["CSRF"],
                "add_media_ids": config["WatchVideoTask"]["FAVORITE_ID"],
                "del_media_ids": ""
            }
            headers = copy.deepcopy(config["pcheaders"])
            headers["Referer"] = "https://www.bilibili.com/av%s" % need_vilst["aid"]
            data = await AsyncioCurl().request_json("POST", url, headers = headers, data = payload)

            if data["code"]:
                Log.error("出现错误 %s" % (data["message"]))
