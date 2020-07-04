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
from Utils import Utils


class GuardRaffle:
    def __init__(self):
        self.last_guard_room = 0
        self.had_gotted_guard = {}
        self.award = {}
        self.last_clear_time = time.time()

    async def clear_had_gotted_guard(self):
        for key in self.had_gotted_guard:
            if self.had_gotted_guard[key] < time.time():
                del self.had_gotted_guard[key]

    async def guard_list(self):
        url = "http://118.25.108.153:8080/guard"
        headers = {
            "User-Agent": "bilibili-live-tools/456562314"
        }
        return await AsyncioCurl().request_json("GET", url, headers = headers)

    async def guard_lottery(self):
        for k in range(3):
            try:
                data = await self.guard_list()
                break
            except Exception as e:
                continue
        else:
            Log.error("连接舰长服务器失败")
            return
        for i in range(0, len(data)):
            GuardId = data[i]['Id']
            if GuardId not in self.had_gotted_guard and GuardId != 0:
                self.had_gotted_guard[GuardId] = data[i]['EndTime']
                OriginRoomId = data[i]['RoomId']
                await self.guard_join(OriginRoomId, GuardId)
                await asyncio.sleep(0.2)

    async def guard_join(self, OriginRoomId, GuardId):
        if not OriginRoomId == self.last_guard_room:
            if not await Utils.is_normal_room(OriginRoomId):
                return
            await BasicRequest.enter_room(OriginRoomId)
            self.last_guard_room = OriginRoomId
        data = await BasicRequest.guard_req_join(OriginRoomId, GuardId)
        if data['code'] == 0:
            # Log.raffle(f"获取到房间 {OriginRoomId} 编号 {GuardId} 的上船奖励: " + (f"{data['data']['award_text']}" if data['data'][
            #     'award_text'] else f"{data['data']['award_name']}X{data['data']['award_num']}"))
            if data['data']['award_text']:
                award_name = data['data']['award_text']
                num = 1
            else:
                award_name = data['data']['award_name']
                num = data['data']['award_num']
            if award_name in self.award:
                self.award[data['data']['award_name']] += num
            else:
                self.award[data['data']['award_name']] = num
        elif data['code'] == -403 and data['msg'] == "访问被拒绝":
            Log.error(f"访问被拒绝：{data['message']}")
            print(data)
        elif data['code'] == 400 and (data['msg'] == "你已经领取过啦" or data['msg'] == "已经过期啦,下次早点吧"):
            # Log.raffle(f"房间 {OriginRoomId} 编号 {GuardId} 的上船奖励已领过")
            pass
        else:
            Log.raffle(f"房间 {OriginRoomId} 编号 {GuardId}  的上船奖励领取出错: {data}")

    async def work(self):
        if config["Function"]["RAFFLE_HANDLER"] == "False" or config["Raffle_Handler"]["GUARD"] == "False":
            return

        Log.info("开启舰长抽奖")
        while True:
            try:
                if time.time() - self.last_clear_time > 600:
                    await self.clear_had_gotted_guard()
                await self.guard_lottery()
                if self.award:
                    raffle_str = f'本次周期抽奖获得：'
                    for award_name in self.award:
                        raffle_str += award_name + 'X{}'.format(self.award[award_name])
                    raffle_str += '，休息 30 s'
                    Log.raffle(raffle_str)
                    self.award = {}
                await asyncio.sleep(30)
            except Exception as e:
                await asyncio.sleep(10)
                Log.error('出现错误 {}'.format(e))
