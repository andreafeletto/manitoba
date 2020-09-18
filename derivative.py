
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


def callback_var(update, context):
    update.message.reply_text('Choose a variable')
    return State.CHOOSE_VAR


def enter_derivative(update, context):
    context.user_data['callbacks'] = [callback_var]
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


derivative_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex('^derivative$'),
            enter_derivative
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
    },
    fallbacks=[CommandHandler('done', done)],
)
