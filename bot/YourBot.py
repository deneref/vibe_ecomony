import telebot
from AnalystApp import AnalystApp
from bot.KeaboardManager import KeaboardManager


class YourBot():

    def __init__(self):
        with open('secrets/tgapi', 'r') as f:
            apikey = f.read()

        self.bot = telebot.TeleBot(apikey)
        self.analystApp = AnalystApp()
        self.keyboardsManager = KeaboardManager()
        self.privacy = False

    def check_entry_id(self, message) -> bool:
        with open('secrets/ids', 'r+') as file:
            ids = file.read().splitlines()
            if message.from_user.id not in ids:
                if not self.privacy:
                    file.write(str(message.from_user.id) + '\n')
                return False

        return True

    def send_main_menu_board(self, id):
        self.bot.send_message(id, "Опции:",
                              reply_markup=self.keyboardsManager.guestMainOptionsKeyboard())

    def startBot(self):
        bot, analystApp = self.bot, self.analystApp

        @bot.message_handler(commands=["start"])
        def handle_start(message):
            frendly_id = self.check_entry_id(message)
            user_id = message.from_user.id
            if not self.privacy:
                if not frendly_id:
                    bot.send_message(user_id, "id записан")

                self.send_main_menu_board(user_id)
            else:
                if not frendly_id:
                    bot.send_message(user_id, "сюда нельзя")
                else:
                    self.send_main_menu_board(user_id)

        @bot.message_handler(func=lambda message: message.text == 'Графики',
                             content_types=['text'])
        def handle_analysis(message):
            print('Получил команду Графики')
            graphs = self.analystApp.getAllGraphs()
            for graph in graphs:
                bot.send_photo(message.chat.id, graph,
                               caption='график')

        @bot.message_handler(func=lambda message: message.text == 'Средняя прибыль по продукту', content_types=['text'])
        def handle_avg_by_product(message):
            print('Получил команду средннее')
            avg = self.analystApp.get_avg_by_product()
            bot.send_message(message.chat.id, avg)

        @bot.message_handler(func=lambda message: message.text == 'ROI breakdown', content_types=['text'])
        def handle_avg_by_product(message):
            print('ROI breakdown')
            roi = self.analystApp.get_roi_breakdown()
            bot.send_message(message.chat.id, roi)

        @bot.message_handler(func=lambda message: message.text == 'Графики документом', content_types=['text'])
        def handle_avg_by_product(message):
            print('Графики документом')
            graphs = self.analystApp.getAllGraphs()
            for graph in graphs:
                bot.send_document(message.chat.id, document=graph,
                                  caption='график')

        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()

        print('запускаю бота')
        bot.polling(none_stop=True)
