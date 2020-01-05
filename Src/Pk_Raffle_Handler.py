# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# PK抽奖处理模块

import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Utils import Utils
from Timer import Timer
from Statistics import Statistics
from BasicRequest import BasicRequest

class PkRaffleHandler:

    @staticmethod
    async def check(real_roomid, raffle_name):
        if not await Utils.is_normal_room(real_roomid, raffle_id=None):
            return
        data = await BasicRequest.pk_req_check(real_roomid)
        # 照搬的TV,等下次大乱斗
        checklen = data["data"]["list"]
        list_available_raffleid = []
        for j in checklen:
            raffle_id = j["raffleId"]
            raffle_type = j["type"]
            time_wanted = j["time_wait"] + int(time.time())

            if not Statistics.is_raffleid_duplicate(raffle_id):
                Log.raffle("本次获取到 %s 的抽奖id为: %s"%(raffle_name,raffle_id))
                list_available_raffleid.append((raffle_id,raffle_type,time_wanted))
                Statistics.add2raffle_ids(raffle_id)
                
        for raffle_id,raffle_type,time_wanted in list_available_raffleid:
            Timer.add2list_jobs(PkRaffleHandler.join,time_wanted,(real_roomid,raffle_id,raffle_type,raffle_name))

    @staticmethod
    async def join(real_roomid,raffle_id,raffle_type,raffle_name):
        await BasicRequest.enter_room(real_roomid)
        data = await BasicRequest.pk_req_join(real_roomid, raffle_id)
        Log.raffle("参与了房间 %s 的 %s 抽奖")
        Statistics.add2joined_raffles("PK类(合计)")

        code = data["code"]
        if not code:
            Log.raffle("房间 %s %s 抽奖结果: %s X %s"%(real_roomid,raffle_name,data["data"]["award_name"],data["data"]["award_num"]))
            Statistics.add2results(data["data"]["award_name"],int(data["data"]["award_num"]))
        elif code == -500:
            Log.error("-500繁忙,稍后重试")
            return False
        elif code == 400:
            Log.error("当前账号正在小黑屋中")
            return False