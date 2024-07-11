import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeaboardManager():

    def guestMainOptionsKeyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Аналитика")
        keyboard.row("Что-то еще")

        return keyboard
