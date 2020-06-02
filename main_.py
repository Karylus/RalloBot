from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from random import randint
import csv
import sys

# http://www.tweepy.org/
import tweepy

# Twitter API codes to getTweets
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


updater = Updater(
    token='', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

#Start command message
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Saludos, usa /quote para conocer mi palabra")

#Unknown commanda message
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="El gran Dios Rallo no comprende ese comando.")

#Gets all Tweets from juanralloquotes and saves them into a csv
def get_tweets(update, context):

    # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # set count to however many tweets you want
    number_of_tweets = 120
    username = 'juanralloquotes'

    # get tweets
    tweets_for_csv = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode="extended").items(number_of_tweets):
        # create array of tweet information: username, tweet id, date/time, text
        tweets_for_csv.append(
            [tweet.full_text.encode('utf-8').decode('utf-8')])

    # write to a new csv file from the array of tweets
    outfile = username + "_tweets.csv"
    print("writing to " + outfile)
    with open(outfile, 'w+') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(tweets_for_csv)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="¡Base de datos actualizada!")

#Sends a quote from the previous generated csv
def quote(update, context):
    randomInt = randint(0, 118)

    with open('juanralloquotes_tweets.csv') as csvDataFile:
        data = list(csv.reader(csvDataFile))
        quote = data[randomInt][0]

    context.bot.send_message(chat_id=update.effective_chat.id, text=quote)


quote_handler = CommandHandler('quote', quote)
dispatcher.add_handler(quote_handler)

getTweets_handler = CommandHandler('update', get_tweets)
dispatcher.add_handler(getTweets_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
