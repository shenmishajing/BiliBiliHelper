import platform

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Utils import Utils
from Timer import Timer
from Statistics import Statistics
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from Raffle_Handler import RaffleHandler
from GuardRaffle import GuardRaffle


class StormRaffleHandler:

    @staticmethod
    async def check(room_id, raffle_id=None):
        if GuardRaffle().get_sleep_time():
            return
        if not await Utils.is_normal_room(room_id):
            return
        if raffle_id is not None:
            data = {"data": {"id": raffle_id}}
        else:
            data = await BasicRequest.storm_req_check(room_id)
        list_available_raffleid = []
        data = data["data"]

        if data:
            raffle_id = data["id"]
            if not Statistics.is_raffleid_duplicate(raffle_id):
                list_available_raffleid.append((raffle_id, 0))
                Statistics.add2raffle_ids(raffle_id)
            for raffle_id, time_wanted in list_available_raffleid:
                Timer.add2list_jobs(StormRaffleHandler.join, time_wanted, (room_id, raffle_id))

    @staticmethod
    async def join(room_id, raffle_id):
        await BasicRequest.enter_room(room_id)
        data = await BasicRequest.storm_req_join(raffle_id)
        Statistics.add2joined_raffles("节奏风暴(合计)")
        if not data["code"]:
            data = data["data"]
            gift_name = data["gift_name"]
            gift_num = data["gift_num"]
            Log.raffle("房间 %s 节奏风暴抽奖结果: %s X %s" % (room_id, gift_name, gift_num))
            Statistics.add2results(gift_name, int(gift_num))
