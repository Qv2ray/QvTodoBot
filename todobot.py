#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random
import os

from telegram import Bot
from telegram.utils.helpers import escape_markdown
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, PicklePersistence)


import todocore
import dart

token = os.getenv('TOKEN')
bot = Bot(token=token)

# Enable logging
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
pickle = PicklePersistence(filename='telegram_data.pickle')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('I love Qv2ray!')


def thank(update, context):
    thank_target = update.message.text.split(' ', 1)[1]
    if thank_target != "":
        update.message.reply_text(f'Thank you so much, {thank_target}!')


def thanks(update, context):
    update.message.reply_text('You\'re welcome!')


def call_cops(update, context):
    emojis = ["👮‍♀️", "👮🏻‍♀️", "👮🏼‍♀️", "👮🏽‍♀️", "👮🏾‍♀️", "👮🏿‍♀️",
              "👮‍♂️", "👮🏻‍♂️", "👮🏼‍♂️", "👮🏽‍♂️", "👮🏾‍♂️", "👮🏿‍♂️",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨",
              "🚓", "🚔", "🚨", "🚓", "🚔", "🚨"]
    text = "📱9️⃣1️⃣1️⃣📲📞👌\n"
    for i in range(random.randint(24, 96)):
        text += random.choice(emojis)
    bot.send_message(update.message.chat_id, text)


def fuck(update, context):
    update.message.reply_text(random.choice(["🍑", "🍆"]))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    todo_engine = todocore.TodoEngine(bot)
    dart_engine = dart.Darter(bot)
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, persistence=pickle, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    for command in todo_engine.getCommands():
        dp.add_handler(command)

    for command in dart_engine.getCommands():
        dp.add_handler(command)

    dp.add_handler(CommandHandler("thank", thank))
    dp.add_handler(CommandHandler("thanks", thanks))
    dp.add_handler(CommandHandler("call_cops", call_cops))
    dp.add_handler(CommandHandler("fuck", fuck))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
