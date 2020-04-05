# BiliBiliHelper Python Version
#感谢TheWanderingCoel大佬的项目
#该模块实现了赛事签到、分享等功能
#本模块由洛水.山岭居室编写

#我很想吐槽：wdnmd不是什么赛事都能用LPL的接口签到啊（雾
#https://github.com/TheWanderingCoel/BiliBiliHelper/issues/43#issuecomment-605611404

import asyncio
import platform
import time

if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from Base import std235959ptm
from Config import *


class MatchTask:

    async def work(self):
        if config["Function"]["MatchTask"] == "False":
            return
        while 1:
            Log.info("检查赛事每日任务")

            await self.LPLTask()
            
            await self.LPLShare()

            await asyncio.sleep(3)
            
            await self.OWLTask() 
            
            await self.OWLShare()

            await asyncio.sleep(3)

            await self.KPLTask() 

            await self.KPLDanmuTask() 

            Log.info("今日全部赛事任务完成")

            if config["MatchTask"]["OpenCapsule"] == "True":
                await self.LPLOpenCapsule()

                await self.OWLOpenCapsule()
                
                await self.KPLOpenCapsule()

            await asyncio.sleep(2*360)

    async def LPLOpenCapsule(self):

        data = await self.GetCapsuleInfo_Request(46)
        if data["data"]["status"] == 0:
            Log.info("开始执行LPL赛事抽奖！")
        else:
            return
        if data["data"]["coin"] <= 0:
            Log.info("诶呀怎么一个抽奖券都没有，下次再来。")
            return

        count = data["data"]["coin"]

        while count >= 1:
            OpenCapsuleCount = 0
            if count < 10:
                OpenCapsuleCount = 1
            elif count < 100:
                OpenCapsuleCount = 10
            elif count >= 100:
                #不懂有钱人
                OpenCapsuleCount = 100
            
            Log.raffle("执行抽奖前拥有: %s 个抽奖券" % (count))
            Log.raffle("本次抽奖前使用: %s 个抽奖券" % (OpenCapsuleCount))

            data = await self.OpenCapsuleById_Request(46,OpenCapsuleCount)
            if(data["code"] == 0):
                for awards in data["data"]["awards"]:
                    Log.raffle("LPL抽奖获得: %s X %s" % (awards["name"], awards["num"]))
            else:
                Log.error("抽奖错误 %s" % (data["message"]))
            #无论如何成功还是失败，都得减，防止死循环
            count = count - OpenCapsuleCount
        Log.info("抽奖完毕，一点都不剩" )

    async def OWLOpenCapsule(self):

        data = await self.GetCapsuleInfo_Request(52)
        if data["data"]["status"] == 0:
            Log.info("开始执行OWL赛事抽奖！")
        else:
            return
        if data["data"]["coin"] <= 0:
            Log.info("诶呀怎么一个抽奖券都没有，下次再来。")
            return

        count = data["data"]["coin"]

        while count >= 1:
            OpenCapsuleCount = 0
            if count < 10:
                OpenCapsuleCount = 1
            elif count < 100:
                OpenCapsuleCount = 10
            elif count >= 100:
                #不懂有钱人
                OpenCapsuleCount = 100
            
            Log.raffle("执行抽奖前拥有: %s 个抽奖券" % (count))
            Log.raffle("本次抽奖前使用: %s 个抽奖券" % (OpenCapsuleCount))

            data = await self.OpenCapsuleById_Request(52,OpenCapsuleCount)
            if(data["code"] == 0):
                for awards in data["data"]["awards"]:
                    Log.raffle("OWL抽奖获得: %s X %s" % (awards["name"], awards["num"]))
            else:
                Log.error("抽奖错误 %s" % (data["message"]))
            #无论如何成功还是失败，都得减，防止死循环
            count = count - OpenCapsuleCount
        Log.info("抽奖完毕，一点都不剩" )

    async def KPLOpenCapsule(self):

        data = await self.GetCapsuleInfo_Request(55)
        if data["data"]["status"] == 0:
            Log.info("开始执行KPL赛事抽奖！")
        else:
            return
        if data["data"]["coin"] <= 0:
            Log.info("诶呀怎么一个抽奖券都没有，下次再来。")
            return

        count = data["data"]["coin"]

        while count >= 1:
            OpenCapsuleCount = 0
            if count < 10:
                OpenCapsuleCount = 1
            elif count < 100:
                OpenCapsuleCount = 10
            elif count >= 100:
                #不懂有钱人
                OpenCapsuleCount = 100
            
            Log.raffle("执行抽奖前拥有: %s 个抽奖券" % (count))
            Log.raffle("本次抽奖前使用: %s 个抽奖券" % (OpenCapsuleCount))

            data = await self.OpenCapsuleById_Request(55,OpenCapsuleCount)
            if(data["code"] == 0):
                for awards in data["data"]["awards"]:
                    Log.raffle("KPL抽奖获得: %s X %s" % (awards["name"], awards["num"]))
            else:
                Log.error("抽奖错误 %s" % (data["message"]))
            #无论如何成功还是失败，都得减，防止死循环
            count = count - OpenCapsuleCount
        Log.info("抽奖完毕，一点都不剩" )
   
    async def KPLTask(self):
        data = await self.GetSignTask_Request(27)
        if data["data"]["status"] == 3:
            Log.info("开始执行KPL赛事签到")
        elif data["data"]["status"] == 6:
            Log.info("今日KPL赛事已经签到")
            return
        else:
            return
        data = await self.MatchSign_Request(21144080,27)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("LPL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))    

    async def LPLTask(self):
        data = await self.GetSignTask_Request(25)
        if data["data"]["status"] == 3:
            Log.info("开始执行OWL赛事签到")
        if data["data"]["status"] == 6:
            Log.info("今日LPL赛事已经签到")
            return
        else:
            return    
        data = await self.MatchSign_Request(7734200,25)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("LPL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))
    
    async def LPLShare(self):
        data = await self.GetShareTask_Request(25)
        if data["data"]["status"] == 3:
            Log.info("开始执行LPL赛事分享")
        if data["data"]["status"] == 6: 
            Log.info("今日LPL赛事已经分享")
            return
        else:
            return
        data = await self.MatchShare_Request(25)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                Log.raffle("LPL分享成功")
            else:
                Log.error("分享错误 %s" % (data["message"]))
        else:
            Log.error("分享错误 %s" % (data["message"]))

    async def OWLTask(self):
        data = await self.GetSignTask_Request(26)
        if data["data"]["status"] == 3:
            Log.info("开始执行OWL赛事签到")
        if data["data"]["status"] == 6: 
            Log.info("OWL赛事已经签到")
            return
        else:
            return
        data = await self.MatchSign_Request(7734200,26)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                for awards in data["data"]["awards"]:
                     Log.raffle("OWL签到获得: %s X %s" % (awards["title"], awards["num"]))
            else:
                 Log.error("签到错误 %s" % (data["message"]))
        else:
            Log.error("签到错误 %s" % (data["message"]))

    async def OWLShare(self):
        data = await self.GetShareTask_Request(26)
        if data["data"]["status"] == 3:
            Log.info("开始执行OWL赛事分享")
        elif data["data"]["status"] == 6: 
            Log.info("OWL赛事已经分享")
            return
        else:
            return

        data = data = await self.MatchShare_Request(26)

        if(data["code"] == 0):
            if data["data"]["status"] == 1:
                Log.raffle("OWL分享成功")
            else:
                Log.error("分享错误 %s" % (data["message"]))
        else:
            Log.error("分享错误 %s" % (data["message"]))

    async def LPLWatch(self):
        #不知道为啥心跳包发过去就看了个寂寞
        #希望有大佬解决，提交Issues或者Pull Requests.
        #感谢你对该项目的贡献
        url = "https://api.live.bilibili.com/xlive/general-interface/v1/lpl-task/GetWatchTask?game_type=25"
        data = await AsyncioCurl().request_json("GET", url ,headers=config["pcheaders"])
        if data["data"]["status"] == 3:
            if data["data"]["progress"]["cur"] != data["data"]["progress"]["max"] :
                Log.info("开始观看LPL直播")      
        if data["data"]["status"] == 6: 
            Log.info("今日LPL直播已经观看完毕") 
            return
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
        data = await self.GetCapsuleInfo_Request(27)
        if data["data"]["status"] == 3:
            if data["data"]["progress"]["cur"] != data["data"]["progress"]["max"] :
                    Log.info("开始发送KPL直播弹幕")
        elif data["data"]["status"] == 6:
            Log.info("今日KPL直播弹幕任务完成")
            return
        else:
            return
        var = 0
        while var <= 3 :
            data = await self.GetDanmuTask_Request(27)
            Log.info("KPL发送弹幕  %s/%s" % (data["data"]["progress"]["cur"], data["data"]["progress"]["max"]))
            if data["data"]["progress"]["cur"] == data["data"]["progress"]["max"] :
                Log.info("KPL发送弹幕完成 获得 抽奖券 X 1")
                var = 0
                break
            else:
                msg = config["MatchTask"]["Message"]
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

    async def GetCapsuleInfo_Request(self,id):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/get_capsule_info_v3?id=" + str(id) + "&from=web"

        data = await AsyncioCurl().request_json("GET", url, headers=config["pcheaders"])

        return data

    async def OpenCapsuleById_Request(self,id,count):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/open_capsule_by_id"

        payload = {
           "id": id,
           "count": count,
           "platform" : "wed",
           "_" : time.time(),
           "csrf_token": account["Token"]["CSRF"],
           "csrf": account["Token"]["CSRF"],
           "visit_id": ""
           }
        
        data = await AsyncioCurl().request_json("POST", url, headers=config["pcheaders"], data=payload)

        return data
