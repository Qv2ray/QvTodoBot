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
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, PicklePersistence)
from emoji import emojize
from datetime import datetime

import parser

token = os.getenv('TOKEN')
bot = Bot(token=token)
# Enable logging
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
pickle = PicklePersistence(filename='telegram_data.pickle')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

# Formatting data


def format_data(data):
    formatted_data = '\n'.join(
        [f'{i + 1}. {data[i]}' for i in range(len(data))])
    return formatted_data


def handle_initial_data(update, context):
    try:
        pickle_data = dict(pickle.get_user_data())[update.message.from_user.id]
        pickle_data_exists = True
    except KeyError:
        pickle_data_exists = False
    if not context.user_data and pickle_data_exists:
        return pickle_data
    else:
        return context.user_data


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('I love Qv2ray!')

# Getting data from JSON (TODO)


def gettodo(update, context):
    user_data = handle_initial_data(update, context)
    try:
        todo_list = user_data['todo']
        message = format_data(todo_list)
        update.message.reply_text(message)
    except Exception:
        message = 'Nothing to do here.'
        update.message.reply_text(message)

# Manipulating data (TODO)

# Add todo


def todo(update, context):
    user_data = handle_initial_data(update, context)
    now = datetime.now()
    formatted_datetime = now.strftime("%Y/%m/%d %H:%M:%S")
    try:
        text = update.message.text.split(' ')[1:]
        if text:
            text = ' '.join(map(str, text))
            if 'todo' not in user_data:
                user_data['todo'] = []
            todo_list = user_data['todo']
            todo_list.append(f'{text} - Created at {formatted_datetime}')
            if not todo_list:
                message = "Nothing to do here."
            else:
                message = format_data(todo_list)

            update.message.reply_text(message)
        else:
            update.message.reply_text('Todo item can not be empty')
    except Exception:
        update.message.reply_text('An error occurred')


def remove(update, context):
    user_data = handle_initial_data(update, context)
    try:
        index = update.message.text.split(' ')[1]
        todo_list = user_data['todo']
        todo_list.pop(int(index) - 1)
        message = format_data(todo_list)
        if message:
            update.message.reply_text(message)
        else:
            update.message.reply_text('Nothing to do')
    except Exception:
        update.message.reply_text('An error occurred')


def toggle(update, context):
    user_data = handle_initial_data(update, context)
    try:
        index = int(update.message.text.split(' ')[1]) - 1
        todo_list = user_data['todo']

        if emojize(":white_heavy_check_mark:") not in todo_list[index]:
            todo_list[index] = f'{todo_list[index]} {emojize(":white_heavy_check_mark:")}'
        else:
            todo_list[index] = todo_list[index].replace(
                emojize(":white_heavy_check_mark:"), '')

        message = format_data(todo_list)
        update.message.reply_text(message)
    except Exception:
        update.message.reply_text('An error occurred')


def dart(update, context):
    text = update.message.text[6:]
    nsp = parser.NumericStringParser()
    try:
        times = int(nsp.eval(text))
    except Exception:
        times = 1
    for i in range(times):
        bot.send_dice(chat_id=update.message.chat_id, emoji='🎯')


def dice(update, context):
    text = update.message.text[6:]
    nsp = parser.NumericStringParser()
    try:
        times = int(nsp.eval(text))
    except Exception:
        times = 1
    for i in range(times):
        bot.send_dice(chat_id=update.message.chat_id, emoji='🎲')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, persistence=pickle, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("todo", todo))
    dp.add_handler(CommandHandler("remove", remove))
    dp.add_handler(CommandHandler("toggle", toggle))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dart", dart))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("gettodo", gettodo))

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
