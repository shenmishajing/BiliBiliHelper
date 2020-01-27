import telegram


class Telegram:

    def __init__(self):
        self.token = notification["Telegram"]["TOKEN"]
        self.chat_id = notification["Telegram"]["CHATID"]
        self.bot = telegram.Bot(token=self.token)

    def send(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)
