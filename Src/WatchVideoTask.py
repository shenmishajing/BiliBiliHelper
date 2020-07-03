import asyncio
import platform
import random
import time
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
    def __init__(self):
        self.ok = 0

    async def work(self):
        if config["Function"]["WatchVideoTask"] == "False":
            return

        while 1:
            Log.info("检查观看视频任务")

            # 必须有房间号才能运行
            if config["WatchVideoTask"]["ROOM_ID"] == "":
                Log.warning("观看视频模块up主号未配置,已停止...")
            else:
                await self.watch()

    async def watch(self):
        var = 0
        while True:
            var += 1
            Log.info("本次观看视频为第 %s 次" % (var))
            Room_Id = random.choice(config["WatchVideoTask"]["ROOM_ID"].split(","))
            Log.info("本次观看选择UP的ID为 %s" % (Room_Id))
            url = "https://api.bilibili.com/x/space/arc/search?ps=100&pn=1&mid=" + str(Room_Id)
            data = await AsyncioCurl().request_json("GET", url)
            need_vilst = random.choice(data["data"]["list"]["vlist"])

            Log.info("本次观看的视频信息如下")
            Log.info("标题  %s" % (need_vilst["title"]))
            Log.info("作者  %s" % (need_vilst["author"]))
            Log.info("视频BV号  %s" % (need_vilst["bvid"]))
            Log.info("视频AV号  %s" % (need_vilst["aid"]))

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

                for i in range(video_duration // 15):
                    payload['played_time'] = payload['real_played_time'] = payload['real_time'] = i * 15
                    data = await AsyncioCurl().request_json("POST", url, headers = headers, data = payload)
                    await asyncio.sleep(15)
                payload['played_time'] = payload['real_played_time'] = payload['real_time'] = video_duration
                data = await AsyncioCurl().request_json("POST", url, headers = headers, data = payload)

            # 看完了给点个赞
            url = "https://api.bilibili.com/x/web-interface/archive/like"
            payload = {
                "aid": need_vilst["aid"],
                "like": 1,
                "csrf": account["Token"]["CSRF"],
                "bvid": need_vilst["bvid"]
            }
            data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

            if (data["code"] == 0):
                Log.info('视频点赞成功')
            else:
                Log.error("出现错误 %s" % (data["message"]))

            # 分享一下
            url = "https://api.bilibili.com/x/web-interface/share/add"

            payload = {
                "aid": need_vilst["aid"],
                "jsonp": "jsonp",
                "csrf": account["Token"]["CSRF"]}

            data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

            if (data["code"] == 0):
                Log.info('视频分享成功')
            else:
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

            if (data["code"] == 0):
                Log.info('视频观看成功')
            else:
                Log.error("出现错误 %s" % (data["message"]))
