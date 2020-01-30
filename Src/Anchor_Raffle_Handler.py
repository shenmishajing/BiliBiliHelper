# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# 天选时刻抽奖处理模块

import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Utils import Utils
from BasicRequest import BasicRequest
from Statistics import Statistics
from Config import *
from Timer import Timer


class AnchorRaffleHandler:

    @staticmethod
    async def check(real_roomid):
        data = await BasicRequest.anchor_req_chcek(real_roomid)
        if not data["code"]:
            data = data["data"]
            if Utils.have_win_award(data["award_users"]):
                Log.raffle("%s 天选时刻抽奖结果: %s" % (real_roomid, data["name"]))
                Statistics.add2results(data["name"], 1)
            else:
                Log.raffle("%s 天选时刻抽奖结果: 没有中奖" % real_roomid)

    @staticmethod
    async def join(data):
        if not Utils.is_normal_room(data["roomid"]):
            return
        if not Utils.is_normal_anchor(data["name"]):
            Log.error("检测到异常的天选时刻")
            return
        data = await BasicRequest.anchor_req_join(data["id"])
        if not data["code"]:
            Log.raffle("参与了 %s 的 天选时刻" % data["roomid"])
            Statistics.add2joined_raffles("天选时刻(合计)")
            Timer.add2list_jobs(AnchorRaffleHandler.join, data["expireAt"], (data["roomid"]))
        else:
            Log.error("%s 天选时刻错误: %s" % (data["roomid"], data["message"]))
