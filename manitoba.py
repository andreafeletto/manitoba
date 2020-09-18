#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Telegram Bot to do math
'''

import logging

from enum import IntEnum, unique, auto

from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    PicklePersistence
)

from derivative import derivative_handler
from integral import integral_handler
from limit import limit_handler
from utils import done

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


def compute(update, context):
    expr_type = context.user_data['expr_type']
    text = 'This is what you typed:'
    if expr_type == 'derivative':
        text += '\nf(x) = {function}'.format(**context.user_data)
        text += '\nx = {var}'.format(**context.user_data)
    update.message.reply_text(text)


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
                derivative_handler,
                integral_handler,
                limit_handler,
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
