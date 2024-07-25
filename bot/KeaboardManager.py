import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeaboardManager():

    def guestMainOptionsKeyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Графики")
        keyboard.row("Графики документом")
        keyboard.row("Средняя прибыль по продукту")
        keyboard.row("ROI breakdown")
        keyboard.row("Update Sheet Аллоцированный расход")

        return keyboard
