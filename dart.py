import parser
from telegram.ext import CommandHandler


class Darter:
    def __init__(self, bot):
        self.bot = bot

    def getCommands(self):
        return [CommandHandler("dart", self.dart),
                CommandHandler("dice", self.dice),
                CommandHandler("basketball", self.basketball),
                CommandHandler("soccer", self.soccer)]

    def dart(self, update, context):
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = parser.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🎯')

    def dice(self, update, context):
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = parser.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🎲')

    def basketball(self, update, context):
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = parser.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='🏀')

    def soccer(self, update, context):
        text = ''.join(map(str, update.message.text.split(' ')[1:]))
        nsp = parser.NumericStringParser()
        try:
            times = int(nsp.eval(text))
        except Exception:
            times = 1
        for i in range(times):
            self.bot.send_dice(chat_id=update.message.chat_id, emoji='⚽️')
