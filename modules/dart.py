import modules.expression as expression
from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackContext
from telegram import Update, Message
from typing import List


class Darter:
    def __init__(self, bot: Bot):
        self.bot = bot

    def getCommands(self) -> List[CommandHandler]:
        return [CommandHandler("dart", self.dart),
                CommandHandler("dice", self.dice),
                CommandHandler("basketball", self.basketball),
                CommandHandler("soccer", self.soccer)]

    def dart(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = expression.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🎯')

    def dice(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = expression.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🎲')

    def basketball(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = expression.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🏀')

    def soccer(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = expression.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='⚽️')
