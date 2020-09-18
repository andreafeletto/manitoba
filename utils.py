
from functools import wraps
from telegram.ext import ConversationHandler


def intermediate(func):
    ''' makes `func` follow the callback stack '''
    @wraps(func)
    def wrapper(update, context):
        func(update, context)
        if callbacks := context.user_data['callbacks']:
            callback = callbacks.pop(0)
            return callback(update, context)
    return wrapper


def done(update, context):
    update.message.reply_text('Bye bye :(')
    return ConversationHandler.END
