# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 该代码实现了定时自动送出过期礼物的功能

import asyncio
import platform
import time

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
            localtime = time.localtime(time.time())
            if self.mode == 1:
                if (localtime.tm_mday != self.today and localtime.tm_hour == int(config["GiftSend"]["TIME"])):
                    status = await self.SendGift()
                    if status == 2 or status == 25014:
                        self.today = localtime.tm_mday
                        # 如果定时送礼有勋章没有填完，得清空轮询，防止第二天轮到的并不是第一个勋章
                        self.index = 0
                        Log.info("本次定时送礼完成，睡眠到明天")
                        await asyncio.sleep(std235959ptm())
                    elif status == 1:
                        return
                await asyncio.sleep(60)

            elif self.mode == 2:
                # 判断是否已经到另一天
                if localtime.tm_mday != self.today:
                    self.today = localtime.tm_mday
                    self.index = 0  # 如果到了清空轮询，防止还是原来的勋章
                status = await self.SendGift()
                if status == 25014:
                    self.today = localtime.tm_mday
                    # 如果定时送礼有勋章没有填完，得清空轮询，防止第二天轮到的并不是第一个勋章
                    self.index = 0
                    Log.info("本次循环送礼完成，睡眠到明天")
                    await asyncio.sleep(std235959ptm())
                elif status == 0 or status == 2:
                    SleepTime = int(-float(config["GiftSend"]["TIME"]) * 3600)
                    Log.info("本次循环送礼完成，睡眠时间 %s s" % SleepTime)
                    await asyncio.sleep(SleepTime)
                elif status == 1:
                    return

    # 返回值
    # 0 没有异常正常结束
    # 1 出现异常退出
    # 2 背包清空完毕
    # 25014 今日任务已完成
    async def SendGift(self):
        status = await self.getRoomInfo()
        send = True
        while status == 0 and send:
            send = False
            Log.info("开始执行自动送礼物...")
            url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
            data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])
            if data["code"] != 0:
                Log.warning("背包查看失败!" + data["message"])
            if len(data["data"]["list"]) != 0:
                for each in data["data"]["list"]:
                    IfExpired = each["expire_at"] >= data["data"]["time"] and each["expire_at"] <= data["data"][
                        "time"] + int(config["GiftSend"]["GIFTTiME"])
                    if IfExpired == True or int(config["GiftSend"]["GIFTTiME"]) == -1:
                        send = True
                        NeedGift = await Utils.value_to_full_intimacy_today(self.roomid)
                        SendGift = each
                        # 1个亿元相当于10个单位的亲密度，所以要除掉一些
                        if each["gift_name"] == "亿元":
                            # 向下取整
                            NeedGift = int(NeedGift / 10)
                            SendGift["gift_num"] = NeedGift
                        # 判断需要的礼物是否过多，避免浪费
                        if each["gift_num"] >= NeedGift:
                            SendGift["gift_num"] = NeedGift
                        await self.send(SendGift)
                        await asyncio.sleep(6)
                        status = await Utils.is_intimacy_full_today(self.roomid)
                        if status:
                            Log.info("当前房间勋章亲密度已满")
                            break
            if not send:
                Log.info("背包清空完毕，退出任务...")
                return 2
            status = await self.getRoomInfo()
        if status == 1:
            Log.warning("清空礼物功能禁用!")
        return status

    # 返回值
    # 0 没有异常正常结束
    # 1 出现异常退出
    # 25014 今日任务已完成
    async def getRoomInfo(self):
        Log.info("正在生成直播间信息...")

        url = "https://api.bilibili.com/x/member/web/account"
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"])

        if "code" in data and data["code"] != 0:
            Log.warning("获取账号信息失败!" + data["message"])
            return 1
        medal_list = config["GiftSend"]["ROOM_ID"].split(",") + [medal[0] for medal in await Utils.fetch_medal(False)]
        while True:
            # 房间轮询
            status = await Utils.is_intimacy_full_today(medal_list[self.index])
            if status:
                Log.warning("当前房间 %s 勋章亲密度已满,尝试切换房间..." % medal_list[self.index])
                if len(medal_list) <= self.index + 1:
                    Log.warning("无其他可用房间，休眠到明天...")
                    return 25014
                else:
                    self.index += 1
            else:
                Log.warning("礼物赠送房间更改为 %s" % medal_list[self.index])
                break

        self.uid = data["data"]["mid"]

        url = "https://api.live.bilibili.com/room/v1/Room/get_info"
        payload = {
            "id": medal_list[self.index]
        }
        data = await AsyncioCurl().request_json("GET", url, headers = config["pcheaders"], params = payload)

        if data["code"] != 0:
            Log.warning("获取主播房间号失败!" + data["message"])
            return 1

        Log.info("直播间信息生成完毕!")

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
        else:
            Log.info("成功向 %s 投喂了 %s 个 %s" % (payload["biz_id"], value["gift_num"], value["gift_name"]))
