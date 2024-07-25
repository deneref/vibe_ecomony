import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeaboardManager():

    def guestMainOptionsKeyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row_width = 3
        keyboard.row("Графики", "ROI breakdown")
        # keyboard.row("Графики документом")
        keyboard.row("Средняя прибыль по продукту",
                     "Update Sheet Аллоцированный расход")
        keyboard.row("Forecast")

        return keyboard
