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
    instance = None

    # 单例模式
    def __new__(cls, *args, **kw):
        def get_time(time_str):
            sec = 0
            factor = 1
            for num in time_str.split(':')[::-1]:
                sec += int(num) * factor
                factor *= 60
            return sec

        if not cls.instance:
            cls.instance = super(GuardRaffle, cls).__new__(cls, *args, **kw)
            cls.instance.last_guard_room = 0
            cls.instance.had_gotted_guard = {}
            cls.instance.award = {}
            cls.instance.last_clear_time = time.time()
            cls.instance.black_status = False
            run_range = config["Raffle_Handler"]["RUN_RANGE"]
            if isinstance(run_range, str):
                run_range = run_range.split(',')
            cls.instance.run_range = []
            for ran in run_range:
                cls.instance.run_range.append([get_time(time_str) for time_str in ran.split('-')])
            cls.instance.run_range.sort(key = lambda item: item[0])
        return cls.instance

    def get_localtime(self):
        localtime = time.localtime(time.time())
        return localtime.tm_sec + 60 * localtime.tm_min + 3600 * localtime.tm_hour

    def get_run_status(self):
        localtime = self.get_localtime()
        for i in range(len(self.run_range)):
            if self.run_range[i][0] <= localtime < self.run_range[i][1] or self.run_range[i][1] < self.run_range[i][
                0] <= localtime or localtime < self.run_range[i][1] < self.run_range[i][0]:
                return True
        return False

    def get_sleep_time(self):
        if self.get_run_status():
            if self.black_status:
                return random.randint(1800, 7200)
            else:
                return 0
        else:
            localtime = self.get_localtime()
            for i in range(len(self.run_range)):
                if localtime < self.run_range[i][0]:
                    return self.run_range[i][0] - localtime
            return 3600 * 24 + self.run_range[0][0] - localtime

    async def clear_had_gotted_guard(self):
        key_list = []
        for key in self.had_gotted_guard:
            if self.had_gotted_guard[key] < time.time():
                key_list.append(key)
        for key in key_list:
            self.had_gotted_guard.pop(key, None)

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
            if GuardId not in self.had_gotted_guard and GuardId != 0 and data[i]['EndTime'] > time.time():
                self.had_gotted_guard[GuardId] = data[i]['EndTime']
                OriginRoomId = data[i]['RoomId']
                res = await self.guard_join(OriginRoomId, GuardId)
                if res == -1:
                    break
                await asyncio.sleep(0.2)

    async def guard_join(self, OriginRoomId, GuardId):
        if not OriginRoomId == self.last_guard_room:
            if not await Utils.is_normal_room(OriginRoomId):
                return
            await BasicRequest.enter_room(OriginRoomId)
            self.last_guard_room = OriginRoomId
        if random.random() * 100 > int(config["Raffle_Handler"]["P"]):
            return
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
            self.black_status = True
            Log.error(f"访问被拒绝：{data}，已进入小黑屋")
            return -1
        elif data['code'] == 400 and (data['msg'] == "你已经领取过啦" or data['msg'] == "已经过期啦,下次早点吧"):
            # Log.raffle(f"房间 {OriginRoomId} 编号 {GuardId} 的上船奖励{data['msg']}")
            pass
        else:
            Log.raffle(f"房间 {OriginRoomId} 编号 {GuardId}  的上船奖励领取出错: {data}")
        return 0

    async def work(self):
        if config["Function"]["RAFFLE_HANDLER"] == "False" or config["Raffle_Handler"]["GUARD"] == "False":
            return

        Log.info("开启舰长抽奖")
        while True:
            try:
                sleep_time = self.get_sleep_time()
                if not sleep_time:
                    if time.time() - self.last_clear_time > 300:
                        Log.info("清理过期抽奖 ID 缓存")
                        await self.clear_had_gotted_guard()
                        self.last_clear_time = time.time()
                    await self.guard_lottery()
                    if self.award:
                        raffle_str = f'本次抽奖周期获得：'
                        for award_name in self.award:
                            raffle_str += award_name + 'X{}'.format(self.award[award_name])
                        Log.raffle(raffle_str)
                        self.award = {}
                    await asyncio.sleep(30)
                else:
                    Log.info("抽奖模块退出活动，睡眠 {} s".format(sleep_time))
                    await asyncio.sleep(sleep_time)
                    self.black_status = True
            except Exception as e:
                await asyncio.sleep(10)
                Log.error('出现错误 {}'.format(e))
