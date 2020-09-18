
from enum import IntEnum, unique, auto

from telegram.ext import (
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
)

from utils import intermediate, done


@unique
class State(IntEnum):
    ''' derivative states '''
    TYPE_FUNC = auto()
    CHOOSE_VAR = auto()
    CHOOSE_LIMIT_VALUE = auto()


def callback_var(update, context):
    update.message.reply_text('Choose a variable')
    return State.CHOOSE_VAR


def callback_limit_value(update, context):
    text = 'Write the value of the limit'
    update.message.reply_text(text)
    return State.CHOOSE_LIMIT_VALUE


def enter_limit(update, context):
    context.user_data['callbacks'] = [
        callback_var,
        callback_limit_value,
    ]
    update.message.reply_text('Type your f(x) of choice')
    return State.TYPE_FUNC


@intermediate
def type_func(update, context):
    func = update.message.text
    context.user_data['function'] = func


@intermediate
def choose_var(update, context):
    var = update.message.text
    context.user_data['var'] = var


@intermediate
def type_limit_value(update, context):
    text = update.message.text
    context.user_data['limit_value'] = text


limit_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex('^limit$'),
            enter_limit,
        )
    ],
    states={
        State.TYPE_FUNC: [
            MessageHandler(
                Filters.text & ~Filters.command,
                type_func
            )
        ],
        State.CHOOSE_VAR: [
            MessageHandler(
                Filters.text & ~Filters.command,
                choose_var
            )
        ],
        State.CHOOSE_LIMIT_VALUE: [
            MessageHandler(
                Filters.text & ~Filters.command,
                type_limit_value
            )
        ],
    },
    fallbacks=[CommandHandler('done', done)],
)
