import asyncio
import platform

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from Base import std235959ptm
from Config import *
from BasicRequest import BasicRequest


class MatchTask:

    async def work(self):
        if config["Function"]["MatchTask"] == "False":
            return
        while 1:
            Log.info("检查赛事每日任务")

            #lpl签到
            data = await self.GetSignTask_Request(25)
            if data["data"]["status"] == 3:
                await self.lpl_task() 
            if data["data"]["status"] == 6:
                Log.info("今日LPL赛事已经签到")
            
            data = await self.GetShareTask_Request(25)
            if data["data"]["status"] == 3:
                await self.lpl_share()
            if data["data"]["status"] == 6: 
                Log.info("今日LPL赛事已经分享") 

            #wdnmd不是什么赛事都能用lpl的接口签到啊（雾
            data = await self.GetSignTask_Request(26)
            if data["data"]["status"] == 3:
                await self.owl_task() 
            if data["data"]["status"] == 6: 
                Log.info("OWL赛事已经签到")   
            
            data = await self.GetShareTask_Request(26)
            if data["data"]["status"] == 3:
                await self.owl_share()
            if data["data"]["status"] == 6: 
                Log.info("OWL赛事已经分享")

            data = await self.GetSignTask_Request(26)
            if data["data"]["status"] == 3:
                await self.kpl_task() 
            if data["data"]["status"] == 6:
                Log.info("今日KPL赛事已经签到")

            data = await self.GetDanmuTask_Request(27)
            if data["data"]["status"] == 3:
                if data["data"]["progress"]["cur"] != data["data"]["progress"]["max"] :
                    Log.info("开始发送KPL直播弹幕")
                    await self.KPLDanmuTask() 
            if data["data"]["status"] == 6:
                Log.info("今日KPL直播弹幕任务完成")

            Log.info("今日全部赛事签到/分享任务完成")
            #注释掉，没用
            #url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetWatchTask?game_type=25"
            #data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])
            #if data["data"]["status"] == 3:
            #    if data["data"]["progress"]["cur"] != data["data"]["progress"]["max"] :
            #        Log.info("开始观看LPL直播")
            #        await self.LPLWatch()
            #if data["data"]["status"] == 6: 
            #    Log.info("今日LPL直播已经观看完毕") 
            #Log.info("今日全部赛事每日任务完成")
            #有一些活动需要比赛开始才能进行，就当这样了
            await asyncio.sleep(60*60)


    async def kpl_task(self):

        data = await self.MatchSign_Request(21144080,27)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("LPL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))    

    async def lpl_task(self):

        data = await self.MatchSign_Request(7734200,25)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("LPL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))
    
    async def lpl_share(self):

        data = await self.MatchShare_Request(25)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                Log.raffle("LPL分享成功")
            else:
                Log.error("分享错误 %s" % (data["message"]))
        else:
            Log.error("分享错误 %s" % (data["message"]))

    async def owl_task(self):

        data = await self.MatchSign_Request(7734200,26)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("OWL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))

    async def owl_share(self):

        data = data = await self.MatchShare_Request(26)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                Log.raffle("OWL分享成功")
            else:
                Log.error("分享错误 %s" % (data["message"]))
        else:
            Log.error("分享错误 %s" % (data["message"]))

    async def LPLWatch(self):
        var = 1
        while var == 1 :
            url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetWatchTask?game_type=25"
            data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])
            Log.info("在线观看赛事 %sm/%sm" % (data["data"]["progress"]["cur"]/60, data["data"]["progress"]["max"]/60))
            if data["data"]["progress"]["cur"] == data["data"]["progress"]["max"] :
                Log.info("开始观看LPL完成 获得 抽奖券 X 1")
                break
            var_a = 1
            while var_a <= 3:
                url = "https://api.live.bilibili.com/relation/v1/Feed/heartBeat"
                myheaders = config["pcheaders"]
                myheaders["Origin"]="https://live.bilibili.com/"
                myheaders["Referer"]="https://live.bilibili.com/6"
                data = await AsyncioCurl().request_json("GET", url, headers=config["pcheaders"])
                if data["code"] != 0:
                    Log.warning("向LPL直播间发送心跳包异常")
                else:
                    Log.info("向LPL直播间发送心跳包成功")
                var_a = var_a + 1
                await asyncio.sleep(60)
            url = "https://api.live.bilibili.com/User/userOnlineHeart"
            payload = {
                "csrf_token": account["Token"]["CSRF"],
                "csrf": account["Token"]["CSRF"],
                "visit_id": ""

                }
            data = await AsyncioCurl().request_json("POST", url, headers=config["pcheaders"], data=payload)
            if data["code"] != 0:
                Log.warning("向LPL直播间发送用户在线心跳包异常")
            else:
                Log.info("向LPL直播间发送用户在线心跳包成功")
            #await asyncio.sleep(60)

    async def KPLDanmuTask(self):
        var = 0
        while var <= 3 :
            data = await self.GetDanmuTask_Request(27)
            Log.info("KPL发送弹幕  %s/%s" % (data["data"]["progress"]["cur"], data["data"]["progress"]["max"]))
            if data["data"]["progress"]["cur"] == data["data"]["progress"]["max"] :
                Log.info("KPL发送弹幕完成 获得 抽奖券 X 1")
                var = 0
                break
            else:
                #发送给爷爬
                msg = "_(:3」∠)_"
                data = await BasicRequest.req_send_danmu(msg, 21144080)
                if data["code"] != 0:
                    Log.warning("向KPL直播间发送弹幕异常")
                else:
                    Log.info("向KPL直播间发送弹幕成功")
                var = var + 1
                await asyncio.sleep(120)
        if(var >= 3):
            Log.info("三次向KPL直播间发送弹幕未能领取，下次一定！")

    async def MatchSign_Request(self,room_id,game_type):
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/MatchSign"

        payload = {
           "room_id": room_id,
           "game_type": game_type,
           "csrf_token": account["Token"]["CSRF"],
           "csrf": account["Token"]["CSRF"],
           "visit_id": ""
           }
        
        data = await AsyncioCurl().request_json("POST", url, headers=config["pcheaders"], data=payload)

        return data

    async def MatchShare_Request(self,game_type):
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/MatchShare"

        payload = {
           "game_type": game_type,
           "csrf_token": account["Token"]["CSRF"],
           "csrf": account["Token"]["CSRF"],
           "visit_id": ""
           }
        
        data = await AsyncioCurl().request_json("POST", url, headers=config["pcheaders"], data=payload)

        return data
    
    async def GetSignTask_Request(self,game_type):
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetSignTask?game_type="+str(game_type)

        data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])

        return data
    
    async def GetShareTask_Request(self,game_type):
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetShareTask?game_type="+str(game_type)

        data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])
        
        return data
    
    async def GetDanmuTask_Request(self,game_type):
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetDanmuTask?game_type="+str(game_type)

        data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])
        
        return data
