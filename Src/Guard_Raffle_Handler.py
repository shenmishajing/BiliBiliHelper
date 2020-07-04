# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 舰长抽奖处理模块

import re
import random
import asyncio
import platform

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Utils import Utils
from Statistics import Statistics
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from Config import *
from Raffle_Handler import RaffleHandler


class GuardRaffleHandler:

    @staticmethod
    async def check(real_roomid, raffle_id = None):
        if not await Utils.is_normal_room(real_roomid):
            return
        if raffle_id is not None:
            data = {"data": [{"id": raffle_id, "time": 65}]}
        else:
            for i in range(10):
                data = await BasicRequest.gift_req_check(real_roomid)
                if data["data"]["guard"]:
                    break
                await asyncio.sleep(1)
            else:
                Log.warning("%s 没有guard或guard已领取" % real_roomid)
                return

            list_available_raffleid = []

            for j in data["data"]["guard"]:
                raffle_id = j["id"]
                if not Statistics.is_raffleid_duplicate(raffle_id):
                    Log.raffle("本次获取到的 %s 房间 大航海 抽奖id为 %s" % (real_roomid, raffle_id))
                    list_available_raffleid.append(raffle_id)
                    Statistics.add2raffle_ids(raffle_id)

            tasklist = []
            num_available = len(list_available_raffleid)
            for raffle_id in list_available_raffleid:
                task = asyncio.ensure_future(GuardRaffleHandler.join(num_available, real_roomid, raffle_id))
                tasklist.append(task)
            if tasklist:
                raffle_results = await asyncio.gather(*tasklist)
                if False in raffle_results:
                    Log.error("繁忙提示,稍后重新尝试")
                    RaffleHandler.push2queue((real_roomid,), GuardRaffleHandler.check)

    @staticmethod
    async def join(num, real_roomid, raffle_id):
        await asyncio.sleep(random.uniform(0.5, min(30, num * 1.3)))
        data = await BasicRequest.guard_req_join(real_roomid, raffle_id)
        Log.raffle("参与了房间 %s 的大航海抽奖" % (real_roomid))
        if not data["code"]:
            Statistics.add2results(data["data"]["award_name"], data["data"]["award_num"])
            Log.raffle("房间 %s 大航海抽奖结果: %s" % (real_roomid, data["message"]))
            Statistics.add2joined_raffles("大航海(合计)")
        else:
            Log.info(data)
