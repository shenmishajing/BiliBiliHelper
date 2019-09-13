import json
import requests
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Base import Sign
from config import config

class Curl():
    def __init__(self):
        # 给一个初始值方便判断
        self.proxies = None
        if config["Proxy"]["PROXY_TYPE"] != "None":
            if config["Proxy"]["PROXY_TYPE"].lower() == "http":
                if config["Proxy"]["PROXY_USERNAME"] != "" and config["Proxy"]["PROXY_PASSWORD"] != "":
                    self.proxies = {
                        "http": "http://" + config["Proxy"]["PROXY_USERNAME"] + ":" + config["Proxy"]["PROXY_PASSWORD"] + "@" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"], 
                        "https": "https://" + config["Proxy"]["PROXY_USERNAME"] + ":" + config["Proxy"]["PROXY_PASSWORD"] + "@" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"]
                    }
                else:
                    self.proxies = {
                        "http": config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"],
                        "https": config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"]
                    }
            elif config["Proxy"]["PROXY_TYPE"].lower() == "socks5":
                if config["Proxy"]["PROXY_USERNAME"] != "" and config["Proxy"]["PROXY_PASSWORD"] != "":
                    self.proxies = {
                    "http": "socks5://" + config["Proxy"]["PROXY_USERNAME"] + ":" + config["Proxy"]["PROXY_PASSWORD"] + "@" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"], 
                    "https": "socks5://" + config["Proxy"]["PROXY_USERNAME"] + ":" + config["Proxy"]["PROXY_PASSWORD"] + "@" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"]
                    }
                else:
                    self.proxies = {
                    "http": "socks5://" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"], 
                    "https": "socks5://" + config["Proxy"]["PROXY_ADDRESS"] + ":" + config["Proxy"]["PROXY_PORT"]
                    }

    def request_json(self,
                     method,
                     url,
                     headers=None,
                     data=None,
                     params=None,
                     sign=True):
        i = 0
        while True:
            i += 1
            if i >= 10:
                    Log.warning(url)
            try:
                if method == "GET":
                    if sign == True:
                        params = Sign(params)
                    if self.proxies != None:
                        r = requests.get(url,headers=headers,params=params,proxies=self.proxies)
                    else:
                        r = requests.get(url,headers=headers,params=params)
                    return json.loads(r.text)
                elif method == "POST":
                    if sign == True:
                        data = Sign(data)
                    if self.proxies != None:
                        r = requests.post(url,headers=headers,data=data,proxies=self.proxies)
                    else:
                        r = requests.post(url,headers=headers,data=data)
                    return json.loads(r.text)
            except Exception as e:
                Log.error(e)
                continue
