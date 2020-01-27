import sys
sys.path.append("..")
import asyncio
import aiohttp

from Config import notification

class ServerChan:

    def __init__(self):
        self.sckey = notification["ServerChan"]["SCKEY"]
        self.url = f"https://sc.ftqq.com/{self.sckey}.send"
        self.session = aiohttp.ClientSession()

    async def send(self, title, content):
        payload = {
            "title": title,
            "desp": content
        }
        data = await self.session.request("POST", self.url, data=payload)
        if not data["errno"]:
            Log.info("通过ServerChan发送消息 %s 成功" % title)
        else:
            Log.error("ServerChan发送信息失败 %s" % data["errmsg"])