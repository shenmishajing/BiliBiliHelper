# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 本文件实现了项目的Unix下日志功能,彩色输出以及写入文件
# 无奈ctypes的那个方法无法在Windows以外系统实现
# 只能写了一个在Unix下实现的日志的模块

import os
import sys
import time
from config import *

class Loggger():

    def __init__(self,filename):
        self.filename = filename
        self.level = {
        "debug":0,
        "info":1,
        "warning":2,
        "error":3,
        "critical":4
        }
        self.current_level = self.level[config["Log"]["LOG_LEVEL"]]
        # 统计日志行数
        self.count = 0

    def debug(self,data,level=0):
        if self.current_level > level:
            return
        data = f"{self.timestamp()} - DEBUG: {data}"
        print("\033[34;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
        self.clean_log()

    def info(self,data,level=1):
        if self.current_level > level:
            return
        data = f"{self.timestamp()} - INFO: {data}"
        print("\033[32;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
        self.clean_log()

    def warning(self,data,level=2):
        if self.current_level > level:
            return
        data = f"{self.timestamp()} - WARNING: {data}"
        print("\033[33;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
        self.clean_log()

    def error(self,data,level=3):
        if self.current_level > level:
            return
        data = f"{self.timestamp()} - ERROR: {data}"
        print("\033[31;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
        self.clean_log()

    def critical(self,data,level=4):
        if self.current_level > level:
            return
        data = f"{self.timestamp()} - CRITICAL: {data}"
        print("\033[35;1m"+data+"\033[0m")
        with open(self.filename,"a",encoding="utf-8") as f:
            f.write(data+"\n")
        self.clean_log()
    
    def timestamp(self):
        str_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        return str_time
    
    def clean_log(self,startup=False,http_delete=False):
        if (self.count > int(config["Log"]["LOG_LIMIT"]) and config["Log"]["AUTO_CLEAN"] == True) or (startup == True or http_delete == True):
            open(os.getcwd()+"/Log/BiliBiliHelper.log", 'w').close()
            self.count = 0
        else:
            self.count += 1

Log = Loggger(os.getcwd()+"/Log/BiliBiliHelper.log")