import os
import logging
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from flask import Flask
from config import config

class API:

    def work(self):
        app = Flask(__name__)

        logging.getLogger('werkzeug').disabled = True
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        
        @app.route("/version")
        def version():
            return "v0.0.2"
        
        Log.info("正在启动API服务...")
        app.logger.disabled = True
        try:
            app.run(threaded=True,
                    port=config["API"]["LISTEN_PORT"])
        except OSError as e:
            Log.error("API服务器启动错误: " + str(e))