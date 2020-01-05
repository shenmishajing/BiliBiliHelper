# BiliBiliHelper Python Version
# Copy right (c) 2019-2020 TheWanderingCoel
# BiliBiliHelper API核心模块

import os
import tailer
import logging
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from flask import Flask, jsonify, request, stream_with_context, Response
from Config import *
from Sentence import Sentence
from Version import version

class API:

    def get_configs(self):
        data = {
            "Function": {
                "capsule": config["Function"]["CAPSULE"],
                "coin2silver": config["Function"]["COIN2SILVER"],
                "dailybag": config["Function"]["DAILYBAG"],
                "giftsend": config["Function"]["GIFTSEND"],
                "group": config["Function"]["GROUP"],
                "silver2coin": config["Function"]["SILVER2COIN"],
                "silverbox": config["Function"]["SILVERBOX"],
                "task": config["Function"]["TASK"],
                "raffle_handler": config["Function"]["RAFFLE_HANDLER"]
            },
            "Coin2Silver": {
                "coin": config["Coin2Silver"]["COIN"]
            },
            "Live": {
                "room_id": config["Live"]["ROOM_ID"]
            },
            "Raffle_Handler": {
                "tv": config["Raffle_Handler"]["TV"],
                "pk": config["Raffle_Handler"]["PK"],
                "guard": config["Raffle_Handler"]["GUARD"],
                "storm": config["Raffle_Handler"]["STORM"]
            },
            "Log": {
                "log_level": config["Log"]["LOG_LEVEL"]
            },
            "Other": {
                "info_message": config["Other"]["INFO_MESSAGE"],
                "sentence": config["Other"]["SENTENCE"]
            },
            "Proxy": {
                "proxy_type": config["Proxy"]["PROXY_TYPE"],
                "proxy_address": config["Proxy"]["PROXY_ADDRESS"],
            },
            "API": {
                "listen_port": config["API"]["LISTEN_PORT"],
                "allow_lan": config["API"]["ALLOW_LAN"]
            },
            "Server": {
                "address": config["Server"]["ADDRESS"],
                "password": config["Server"]["PASSWORD"]
            }

        }
        return jsonify(data)

    def get_log(self):
        for line in tailer.follow(open(os.getcwd()+"/Log/BiliBiliHelper.log")):
            data = {
                "message": line
            }
            yield str(data) + "\n"
    
    def work(self):

        app = Flask(__name__)

        logging.getLogger('werkzeug').disabled = True
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        
        @app.route("/",methods=["GET"])
        def hello():
            data = {
                "hello": "BiliBiliHelper"
            }
            return jsonify(data)
        
        @app.route("/version",methods=["GET"])
        def version():
            data = {
                "version": version
            }
            return jsonify(data)
        
        @app.route("/sentence",methods=["GET"])
        def sentence():
            data = {
                "sentence": Sentence().get_sentence()
            }
            return jsonify(data)

        @app.route("/configs",methods=["GET", "PATCH", "PUT"])
        def configs():
            if request.method == "GET":
                return self.get_configs()
            elif request.method == "PATCH":
                return
            elif request.method == "PUT":
                return

        @app.route("/logs",methods=["GET","DELETE"])
        def logs():
            if request.method == "GET":
                return Response(stream_with_context(self.get_log()),content_type='application/json')
            elif request.method == "DELETE":
                try:
                    Log.clean_log(http_delete=True)
                    data = {
                        "status": "OK"
                    }
                    return jsonify(data)
                except Exception as e:
                    data = {
                        "status": str(e)
                    }
                    return jsonify(data)
        
        Log.info("正在启动API服务...")
        app.logger.disabled = True
        # 从配置文件导入配置
        app.config.from_pyfile(os.getcwd()+"/Conf/Flask.conf")
        try:
            app.run(threaded=True,
                    port=config["API"]["LISTEN_PORT"])
        except OSError as e:
            Log.error("API服务器启动错误: " + str(e))