"""
    Main Telegram Chatbot Programs
    Created by: Anang Faturrohman @anang42429@gmail.com
"""

from telegram import Update, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler
import prettytable as pt

from logx.data.settings_handler import TelegramSetting
from logx.data.database_handler import Database

updater = Updater(str(TelegramSetting.token), use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    r"""Handler for user when typing \'/start\'."""
    print(f"Chat Id: {update.effective_chat.id}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, i\'m your personal assistant")


def yell(update: Update, context: CallbackContext):
    r"""Handler for \'/yell\' command."""
    text_caps = ' '.join(context.args).upper()
    print(f"Chat Id: {update.effective_chat.id}, Message: {text_caps})")
    print(f"Context: {context.args}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def ask(update: Update, context: CallbackContext):
    r"""Handler for \'ask\' command."""

    print(f"Context {context.args}")
    update.message.reply_text("Oke! Please wait a second...")

    d = Database()
    res = d.get(' '.join(context.args)).VALUE
    if res:
        table = pt.PrettyTable(['NUM', 'NAME', 'TRX', 'TRF', 'DIFF', 'NOTE'])
        table.title = res._date.result['display']
        table.align['NUM'] = 'l'
        table.align['NAME'] = 'l'
        table.align['TRX'] = 'l'
        table.align['TRF'] = 'l'
        table.align['DIFF'] = 'l'
        table.align['NOTE'] = 'l'

        for num, val in enumerate(res.records):
            table.add_row([num + 1, val.cname, val.trx_idr, val.trf_idr, val.diff_idr, val.note])
        
        table.add_row(["","","","","",""])
        table.add_row(["","TOTAL",res.total_idr,"","",""])

        update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("I\'m sorry but currently there are no record on this date!")


start_handler = CommandHandler('start', start)
yell_handler = CommandHandler('yell', yell)
ask_handler = CommandHandler('ask', ask)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(yell_handler)
dispatcher.add_handler(ask_handler)

updater.start_polling()
