from .types import UserData
from emoji import emojize
from datetime import datetime
from telegram import Update, Message
from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackContext


def format_data(data):
    formatted_data = '\n'.join(
        [f'{i + 1}. {data[i]}' for i in range(len(data))])
    return formatted_data


class TodoEngine:
    def __init__(self, bot: Bot):
        self.bot = bot

    def getCommands(self) -> list[CommandHandler]:
        return [CommandHandler("gettodo", self.gettodo),
                CommandHandler("todo", self.todo),
                CommandHandler("remove", self.remove),
                CommandHandler("toggle", self.toggle)]

    def gettodo(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data = UserData(context.user_data)
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
        user_data = UserData(context.user_data)
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            text = update.message.text.split(' ')[1:]
            if text:
                text = ' '.join(map(str, text))
                if 'todo' not in user_data:
                    user_data['todo'] = []
                todo_list = user_data['todo']
                todo_list.append(
                    f'{text} - Created at UTC {formatted_datetime}')
                if not todo_list:
                    message = "Nothing to do here."
                else:
                    message = format_data(todo_list)

                update.message.reply_text(message)
            else:
                update.message.reply_text('Todo item can not be empty')
        except Exception as e:
            update.message.reply_text('An error occurred')
            print(repr(e))

    def remove(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data = UserData(context.user_data)
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

    def toggle(self, update: Update, context: CallbackContext):
        assert isinstance(update.message, Message)
        assert isinstance(update.message.text, str)
        user_data = UserData(context.user_data)
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
