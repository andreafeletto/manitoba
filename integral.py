
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
    CHOOSE_INT_LIMITS = auto()


def callback_var(update, context):
    update.message.reply_text('Choose a variable')
    return State.CHOOSE_VAR


def callback_integration_limits(update, context):
    text = 'Write the limits of integration separated by a comma'
    update.message.reply_text(text)
    return State.CHOOSE_INT_LIMITS


def enter_integral(update, context):
    context.user_data['callbacks'] = [
        callback_var,
        callback_integration_limits,
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
def type_integration_limits(update, context):
    text = update.message.text
    limits = [limit.strip() for limit in text.split(',')]
    context.user_data['limits'] = limits


integral_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex('^integral$'),
            enter_integral
        ),
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
        State.CHOOSE_INT_LIMITS: [
            MessageHandler(
                Filters.text & ~Filters.command,
                type_integration_limits
            )
        ],
    },
    fallbacks=[CommandHandler('done', done)],
)
