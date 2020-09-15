#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Telegram Bot to do math
'''

import logging

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

HOME, CALCULUS = range(2)

home_keyboard = [
    ['derivative'],
    ['derivative'],
    ['derivative']
]
home_markup = ReplyKeyboardMarkup(home_keyboard, one_time_keyboard=True)


def start(update, context):
    reply_text = 'Ciao, io sono manitoba!!'
    update.message.reply_text(reply_text, reply_markup=home_markup)
    return HOME


def operation(update, context):
    op = update.message.text
    context.user_data['operation'] = op
    update.message.reply_text('Type your f(x) of choice')
    return CALCULUS


def done(update, context):
    update.message.reply_text('Bye bye :(')
    return ConversationHandler.END


def main():
    with open('token', 'r') as f:
        token = f.read().strip()

    pickle = PicklePersistence(filename='manitobabot')

    updater = Updater(token=token, persistence=pickle, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            HOME: [
                MessageHandler(
                    Filters.regex('^(derivative|integral|limit)$'),
                    operation
                )
            ]
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
