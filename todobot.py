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
import os

from telegram import Bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence)

token = os.getenv('TOKEN')
bot = Bot(token=token)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)
reply_keyboard = [
    ['Add todo', 'Remove todo'],
    ['Update todo', 'Toggle todo'],
    ['Done']
]
markup = ReplyKeyboardMarkup(reply_keyboard)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('I love Qv2ray!')


def todo(update, context):
    update.message.reply_text('TBD', reply_markup=markup)
    return CHOOSING

# Getting data from JSON


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text

    return TYPING_REPLY

# Manipulating data


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
#    del user_data['choice']

    update.message.reply_text(user_data,
                              reply_markup=markup)

    return CHOOSING

# Saving data to JSON


def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    user_data.clear()
    return ConversationHandler.END


def dart(update, context):
    text = update.message.text
    try:
        times = text.split(' ')[1]
    except IndexError:
        times = 1
    for i in range(int(times)):
        bot.send_dice(chat_id=update.message.chat_id, emoji='🎯')


def dice(update, context):
    text = update.message.text
    try:
        times = text.split(' ')[1]
    except IndexError:
        times = 1
    for i in range(int(times)):
        bot.send_dice(chat_id=update.message.chat_id, emoji='🎲')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Add todo|Remove todo)$'),
                                      regular_choice)
                       ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("todo", todo))
    dp.add_handler(CommandHandler("dart", dart))
    dp.add_handler(CommandHandler("dice", dice))

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
