from custom_types import UserData
from emoji import emojize
from datetime import datetime
from telegram import Update, Message
from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackContext
from typing import List


def format_data(data):
    formatted_data = '\n'.join(
        [f'{i + 1}. {data[i]}' for i in range(len(data))])
    return formatted_data


def parse_index(index):
    try:
        return int(index)
    except ValueError:
        return None


class TodoEngine:
    def __init__(self, bot: Bot):
        self.bot = bot

    def getCommands(self) -> List[CommandHandler]:
        return [CommandHandler("gettodo", self.gettodo),
                CommandHandler("todo", self.todo),
                CommandHandler("remove", self.remove),
                CommandHandler("toggle", self.toggle)]

    def gettodo(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data: UserData = context.user_data
        try:
            todo_list = user_data['todo']
            message = format_data(todo_list)
            update.message.reply_text(message)
        except Exception:
            message = 'Nothing to do here.'
            update.message.reply_text(message)

    def todo(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data: UserData = context.user_data
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            if update.message.reply_to_message is not None:
                from_user = update.message.reply_to_message.from_user['username']
                message = update.message.reply_to_message.text.strip()
                if len(message) == 0:
                    update.message.reply_text('Todo item can not be empty')
                    return
                message = f'{message} @{from_user}'
            else:
                parsed_message = update.message.text.split(' ', 1)
                if len(parsed_message) < 2:
                    update.message.reply_text('Todo item can not be empty')
                    return
                message = parsed_message[1]
            if 'todo' not in user_data:
                user_data['todo'] = []
            todo_list = user_data['todo']
            todo_list.append(
                f'{message} - Created at UTC {formatted_datetime}')
            if not todo_list:
                message = "Nothing to do here."
            else:
                message = format_data(todo_list)
            update.message.reply_text(message)
        except Exception as e:
            update.message.reply_text('An error occurred.')
            print(repr(e))

    def remove(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data: UserData = context.user_data
        todo_list = user_data['todo']
        try:
            parsed_message = update.message.text.split(' ', 1)
            if len(parsed_message) == 2:
                index = parse_index(parsed_message[1])
                if (index is not None and index > 0 and index <= len(todo_list)):
                    index -= 1
                    todo_list.pop(index)
                    message = format_data(todo_list)
                    if message:
                        update.message.reply_text(message)
                    else:
                        update.message.reply_text('Nothing to do')
                else:
                    update.message.reply_text("Invalid index.")
            else:
                update.message.reply_text("You must specify an index.")
        except Exception:
            update.message.reply_text('An error occurred.')

    def toggle(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data: UserData = context.user_data
        todo_list = user_data['todo']
        try:
            parsed_message = update.message.text.split(' ', 1)
            if len(parsed_message) == 2:
                index = parse_index(parsed_message[1])
                if (index is not None and index > 0 and index <= len(todo_list)):
                    index -= 1
                    if emojize(":white_heavy_check_mark:") not in todo_list[index]:
                        todo_list[index] = f'{todo_list[index]} {emojize(":white_heavy_check_mark:")}'
                    else:
                        todo_list[index] = todo_list[index].replace(
                            emojize(":white_heavy_check_mark:"), '')
                    message = format_data(todo_list)
                    update.message.reply_text(message)
                else:
                    update.message.reply_text("Invalid index.")
            else:
                update.message.reply_text("You must specify an index.")
        except Exception:
            update.message.reply_text('An error occurred.')
