import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeaboardManager():

    def guestMainOptionsKeyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Графики")
        keyboard.row("Средняя прибыль по продукту")
        keyboard.row("ROI breakdown")

        return keyboard
