import random
from typing import List
from telegram import Update, Message
from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackContext

class HaveSomeFun:
    def __init__(self, bot: Bot):
        self.bot = bot

    def getCommands(self) -> list[CommandHandler]:
        return [CommandHandler("thank", self.thank),
                CommandHandler("thanks", self.thanks),
                CommandHandler("call_cops", self.call_cops),
                CommandHandler("fuck", self.fuck)]

    def thank(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        thank_target = update.message.text.split(' ', 1)[1]
        if thank_target != "":
            self.bot.send_message(update.message.chat_id,
                                  f'Thank you so much, {thank_target}!')
        else:
            update.message.reply_text('You must specify a target to thank!')

    def thanks(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        update.message.reply_text('You\'re welcome!')

    def call_cops(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        emojis: List[str] = ["👮‍♀️", "👮🏻‍♀️", "👮🏼‍♀️", "👮🏽‍♀️", "👮🏾‍♀️", "👮🏿‍♀️",
                            "👮‍♂️", "👮🏻‍♂️", "👮🏼‍♂️", "👮🏽‍♂️", "👮🏾‍♂️", "👮🏿‍♂️",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
                            "🚓", "🚔", "🚨", "🚓", "🚔", "🚨"]
        text: str = "📱9️⃣1️⃣1️⃣📲📞👌\n"
        for i in range(random.randint(24, 96)):
            text += random.choice(emojis)
        self.bot.send_message(update.message.chat_id, text)

    def eat(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        eater = update.message.from_user['username']
        eat_target = update.message.reply_to_message.from_user['username']
        if eat_target != "":
            self.bot.send_message(update.message.chat_id,
                                  f'{eater} has eaten {eat_target}! 🍴😋')
        else:
            update.message.reply_text('You must reply to the target you want to eat!')

    def fuck(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        update.message.reply_text(random.choice(["🍑", "🍆"]))
