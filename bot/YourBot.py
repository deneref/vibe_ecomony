import telebot
from AnalystApp import AnalystApp


class YourBot():

    def __init__(self):
        with open('secrets/tgapi', 'r') as f:
            apikey = f.read()

        self.bot = telebot.TeleBot(apikey)
        self.analystApp = AnalystApp()
        self.privacy = False

    def check_entry_id(self, message) -> bool:
        with open('secrets/ids', 'r+') as file:
            ids = file.read().splitlines()
            if message.from_user.id not in ids:
                if not self.privacy:
                    file.write(str(message.from_user.id) + '\n')
                return False

        return True

    def startBot(self):
        bot, analystApp = self.bot, self.analystApp

        @bot.message_handler(commands=["start"])
        def handle_start(message):
            frendly_id = self.check_entry_id(message)
            if not self.privacy:
                if not frendly_id:
                    bot.send_message(message.from_user.id, "id записан")
            else:
                if not frendly_id:
                    bot.send_message(message.from_user.id, "сюда нельзя")

        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()

        print('запускаю бота')
        bot.polling(none_stop=True)
