# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 该代码实现了定时自动送出过期礼物的功能

import asyncio
import platform
import time
import copy

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from Base import std235959ptm, std235959
from Config import *
from Utils import Utils


class GiftSend:

    def __init__(self):
        self.index = 0
        self.uid = 0
        self.ruid = 0
        self.roomid = 0
        self.today = 0
        self.mode = 0
        self.gift = {}

    async def work(self):

        if config["Function"]["GIFTSEND"] == "False":
            return
        if config["GiftSend"]["ROOM_ID"] == "":
            Log.warning("自动送礼模块房间号未配置,已停止...")
            return

        if float(config["GiftSend"]["TIME"]) >= 0 and float(config["GiftSend"]["TIME"]) < 24:
            # 定时送礼模式
            self.mode = 1
        elif float(config["GiftSend"]["TIME"]) < 0:
            # 循环送礼模式
            self.mode = 2
        else:
            # 一脸懵逼模式
            Log.warning("定时送礼时间配置错误,已停止...")
            return

        while 1:
            try:
                localtime = time.localtime(time.time())
                if self.mode == 1:
                    if (localtime.tm_mday != self.today and localtime.tm_hour == int(config["GiftSend"]["TIME"])):
                        status = await self.SendGift()
                        if status == 2 or status == 25014:
                            self.today = localtime.tm_mday
                            Log.info("本次定时送礼完成，睡眠到明天")
                            await asyncio.sleep(std235959ptm())
                        elif status == 1:
                            return
                    await asyncio.sleep(60)

                elif self.mode == 2:
                    # 判断是否已经到另一天
                    if localtime.tm_mday != self.today:
                        self.today = localtime.tm_mday
                    status = await self.SendGift()
                    if status == 25014:
                        self.today = localtime.tm_mday
                        Log.info("本次循环送礼完成，睡眠到明天")
                        await asyncio.sleep(std235959ptm())
                    elif status in [0, -1]:
                        SleepTime = int(-float(config["GiftSend"]["TIME"]) * 3600)
                        Log.info("本次循环送礼完成，睡眠时间 %s s" % SleepTime)
                        await asyncio.sleep(SleepTime)
                    elif status == 1:
                        return
            except Exception as e:
                Log.error(e)

    # 返回值
    # 0 没有异常正常结束
    # 1 出现异常退出
    # 2 背包清空完毕
    # 25014 今日任务已完成
    async def SendGift(self):
        Log.info("开始执行自动送礼物...")
        self.gift = {}
        status = await self.getRoomInfo()
        send = True
        while status == 0 and send:
            send = False
            url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
            data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])
            if data["code"] != 0:
                Log.warning("背包查看失败!" + data["message"])
            if len(data["data"]["list"]) != 0:
                medal_status = await Utils.get_medal_light_status([self.roomid])
                if medal_status[self.roomid] == 0 and any([each["gift_id"] == 30607 for each in data["data"]["list"]]):
                    for each in data["data"]["list"]:
                        IfExpired = each["expire_at"] >= data["data"]["time"] and each["expire_at"] <= data["data"][
                            "time"] + int(config["GiftSend"]["GIFTTiME"])
                        if IfExpired == True or int(config["GiftSend"]["GIFTTiME"]) == -1:
                            send = True
                            SendGift = copy.deepcopy(each)
                            # 1个小心心相当于50个单位的亲密度
                            if each["gift_id"] == 30607:
                                SendGift["gift_num"] = 1
                            else:
                                continue
                            await self.send(SendGift)
                            await asyncio.sleep(6)
                            break
                else:
                    for each in data["data"]["list"]:
                        IfExpired = each["expire_at"] >= data["data"]["time"] and each["expire_at"] <= data["data"][
                            "time"] + int(config["GiftSend"]["GIFTTiME"])
                        if IfExpired == True or int(config["GiftSend"]["GIFTTiME"]) == -1:
                            NeedGift = await Utils.value_to_full_intimacy_today(self.roomid)
                            if not medal_status[self.roomid]:
                                NeedGift -= 50
                            SendGift = copy.deepcopy(each)
                            # 1个亿元相当于10个单位的亲密度
                            if each["gift_id"] == 6:
                                # 向下取整
                                NeedGift = int(NeedGift / 10)
                                SendGift["gift_num"] = min(NeedGift, each["gift_num"])
                            # 1个小心心相当于50个单位的亲密度
                            elif each["gift_id"] == 30607 and IfExpired:
                                # 向下取整
                                NeedGift = int(NeedGift / 50)
                                SendGift["gift_num"] = min(NeedGift, each["gift_num"])
                            # 辣条和激爽刨冰等1个单位亲密度的礼物
                            elif each["gift_id"] in [1, 30610]:
                                SendGift["gift_num"] = min(NeedGift, each["gift_num"])
                            else:
                                continue
                            send = True
                            await self.send(SendGift)
                            await asyncio.sleep(6)
                            status = await Utils.is_intimacy_full_today(self.roomid)
                            if status:
                                break
            if not send:
                break
            status = await self.getRoomInfo()
        if self.gift:
            Log.info("本次送礼物周期：")
            for key, gift in self.gift.items():
                for name, num in gift.items():
                    Log.info("向 %s 投喂了 %s 个 %s" % (key, num, name))
        if status == 1:
            Log.warning("清空礼物功能禁用!")
        return status

    # 返回值
    # 0 没有异常正常结束
    # 1 出现异常退出
    # 25014 今日任务已完成
    async def getRoomInfo(self):
        url = "https://api.bilibili.com/x/member/web/account"
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])

        if "code" in data and data["code"] != 0:
            Log.warning("获取账号信息失败!" + data["message"])
            return 1

        self.uid = data["data"]["mid"]

        url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])
        if data["code"] != 0:
            Log.warning("背包查看失败!" + data["message"])

        medal_light_status = await Utils.get_medal_light_status()
        if isinstance(config["GiftSend"]["ROOM_ID"], list):
            medal_list = [int(medal) for medal in config["GiftSend"]["ROOM_ID"] if int(medal) in medal_light_status]
        else:
            medal_list = [int(medal) for medal in config["GiftSend"]["ROOM_ID"].split(", ") if
                          int(medal) in medal_light_status]
        medal_list += [medal[0] for medal in await Utils.fetch_medal(False) if medal[0] not in medal_list]
        self.index = 0
        if any([not medal for medal in medal_light_status.values()]) and any(
                [each["gift_id"] == 30607 for each in data["data"]["list"]]):
            while True:
                # 房间轮询
                if medal_light_status[medal_list[self.index]] != 0:
                    if len(medal_list) <= self.index + 1:
                        self.index = 0
                    else:
                        self.index += 1
                else:
                    break
        else:
            medal_feed_status = await Utils.get_medal_feed_status(medal_list)
            while True:
                # 房间轮询
                if medal_feed_status[medal_list[self.index]]["today_intimacy"] + (
                        1 - medal_light_status[medal_list[self.index]]) * 50 >= \
                        medal_feed_status[medal_list[self.index]][
                            "day_limit"]:
                    if len(medal_list) <= self.index + 1:
                        if any([not medal_light_status[medal] for medal in medal_list]):
                            return -1
                        else:
                            Log.warning("无其他可用房间，休眠到明天...")
                            return 25014
                    else:
                        self.index += 1
                else:
                    break

        url = "https://api.live.bilibili.com/room/v1/Room/get_info"
        payload = {
            "id": medal_list[self.index]
        }
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"], params = payload)

        if data["code"] != 0:
            Log.warning("获取主播房间号失败!" + data["message"])
            return 1

        self.ruid = data["data"]["uid"]
        self.roomid = data["data"]["room_id"]

        return 0

    async def send(self, value):
        url = "https://api.live.bilibili.com/gift/v2/live/bag_send"
        csrf = account["Token"]["CSRF"]

        payload = {
            "coin_type": "silver",
            "gift_id": value["gift_id"],
            "ruid": self.ruid,
            "uid": self.uid,
            "biz_id": self.roomid,
            "gift_num": value["gift_num"],
            "data_source_id": "",
            "data_behavior_id": "",
            "bag_id": value["bag_id"],
            "csrf_token": csrf,
            "csrf": csrf
        }
        data = await AsyncioCurl().request_json("POST", url, headers = config["pcheaders"], data = payload)

        if data["code"] != 0:
            Log.warning("送礼失败!" + data["message"])
        if self.roomid not in self.gift:
            self.gift[self.roomid] = {}
        if value["gift_name"] not in self.gift[self.roomid]:
            self.gift[self.roomid][value["gift_name"]] = value["gift_num"]
        else:
            self.gift[self.roomid][value["gift_name"]] += value["gift_num"]
        Log.debug(f'向 {self.roomid} 送出 {value["gift_num"]} 个 {value["gift_name"]}')
