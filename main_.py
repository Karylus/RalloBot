from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from random import randint
import csv


updater = Updater(
    token='Enter your Token here', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Saludos, usa /quote para conocer mi palabra")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="El gran Dios Rallo no comprende ese comando.")


def quote(update, context):
    randomInt = randint(0, 101)

    with open('juanralloquotes_tweets.csv') as csvDataFile:
    	data=list(csv.reader(csvDataFile))
    	quote = data[randomInt][0]
    	
    context.bot.send_message(chat_id=update.effective_chat.id, text=quote)


quote_handler = CommandHandler('quote', quote)
dispatcher.add_handler(quote_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
