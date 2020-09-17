#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Telegram Bot to do math
'''

import logging

from enum import IntEnum, unique, auto
from functools import wraps

from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    PicklePersistence
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


@unique
class State(IntEnum):
    ''' bot states '''
    HOME = auto()
    TYPE_FUNC = auto()
    CHOOSE_VAR = auto()
    CHOOSE_INT_LIMITS = auto()
    CHOOSE_LIMIT_VALUE = auto()


home_keyboard = [
    ['derivative'],
    ['integral'],
    ['limit']
]
home_markup = ReplyKeyboardMarkup(home_keyboard, one_time_keyboard=True)

def start(update, context):
    reply_text = 'Ciao, io sono manitoba!!'
    update.message.reply_text(reply_text, reply_markup=home_markup)
    return State.HOME


def callback_var(update, context):
    update.message.reply_text('Choose a variable')
    return State.CHOOSE_VAR


def callback_integration_limits(update, context):
    text = 'Write the limits of integration separated by a comma'
    update.message.reply_text(text)
    return State.CHOOSE_INT_LIMITS


def callback_limit_value(update, context):
    text = 'Write the value of the limit'
    update.message.reply_text(text)
    return State.CHOOSE_LIMIT_VALUE


expr_type_callbacks = {
    'derivative': [
        callback_var,
    ],
    'integral': [
        callback_var,
        callback_integration_limits,
    ],
    'limit': [
        callback_var,
        callback_limit_value,
    ]
}

def choose_expr_type(update, context):
    expr_type = update.message.text
    context.user_data['expr_type'] = expr_type
    context.user_data['callbacks'] = expr_type_callbacks[expr_type]
    update.message.reply_text('Type your f(x) of choice')
    return State.TYPE_FUNC


def intermediate(func):
    ''' makes `func` follow the callback stack '''
    @wraps(func)
    def wrapper(update, context):
        func(update, context)
        if callbacks := context.user_data['callbacks']:
            callback = callbacks.pop(0)
            return callback(update, context)
        else:
            return compute(update, context)
    return wrapper


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


@intermediate
def type_limit_value(update, context):
    text = update.message.text
    context.user_data['limit_value'] = text


def compute(update, context):
    expr_type = context.user_data['expr_type']
    text = 'This is what you typed:'
    if expr_type == 'derivative':
        text += 'f(x) = {function}\n'.format(**context.user_data)
        text += 'x = {var}\n'.format(**context.user_data)
    update.message.reply_text(text)


def done(update, context):
    update.message.reply_text('Bye bye :(')
    return ConversationHandler.END


def main():
    with open('token', 'r') as file:
        token = file.read().strip()

    pickle = PicklePersistence(filename='manitobabot')

    updater = Updater(token=token, persistence=pickle, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            State.HOME: [
                MessageHandler(
                    Filters.regex('^(derivative|integral|limit)$'),
                    choose_expr_type
                )
            ],
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
            State.CHOOSE_LIMIT_VALUE: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    type_limit_value
                )
            ],
        },
        fallbacks=[CommandHandler('done', done)],
        name='main_conversation',
        persistent=True
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
