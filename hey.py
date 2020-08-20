import logging
import requests
import random
import re
import os

from collections import deque
from bs4 import BeautifulSoup
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

url = "https://www.pornhub.com/video/search?search="

q=deque()
q.append('/renee_gracie')
q.append('/alli_haze')
q.append('/alex_grey')
q.append('/nicole_aniston')
q.append('/jessa_rhodes')
q.append('/dani_daniels')
q.append('/gina_valentina')
q.append('/kenna_james')
q.append('/tori_black')
q.append('/tiffany_thompson')
q.append('/mia_malakova')
q.append('/lily_carter')
q.append('/kali_roses')
q.append('/alexandra_daddario')
q.append('/sunny_leone')
q.append('/abella_danger')
q.append('/mia_khalifa')
q.append('/lana_rhoades')
q.append('/leah_gotti')
q.append('/little_caprice')

bad_replies = ["Ye dhude,\nSend a number in between 1 to 20.",
                   "MC,\nSend number that's less than 21.",
                   "Bosdike, Dhimaak kaha lagaake rakka hain\n1 se 20 ke andar ek number likh.",
                   "Senorita,\nMy range is 1 to 20.",
                   "Dear User,\nPlease press a number which is greater than 1 but less than 20."
                ]
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    reply_keyboard = [['/vids', '/help'], ['/Trending', '/Viewed'], ['/Recent', '/Subscribed']]
    update.message.reply_text("Welcomo,\nI list you vids from PH, nnjayy...", 
                              reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    update.message.reply_text("By default vids i show you is 3.\nWanna change..?? use /vids\nFor help use /help")
    
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("/start - Welcome Message\n"
                              "/vids - Set number for vids to list\n"
                              "/recent - Lists last 15 search results\n"
                              "/trending - Lists Top Trending PH Players\n"
                              "/viewed - Lists Most viewed PH Players\n"
                              "/subscribed - Lists Most subscribed PH Players")

def vids(update, context):
    reply_keyboard = [['2', '4', '6', '8', '10'], ['12', '14', '16', '18', '20']]
    update.message.reply_text("Senora/Senorita, choose a number for vids:\n(a number in between 1 to 20)", 
                              reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
def set_vids(update, context):
    key = update.message.chat.id
    value = int(update.message.text)
    if value >0 and value <21:
        context.user_data[key] = value    
        update.message.reply_text("You need {} vids?\nTake {}!  Njaaayy...".format(value, value), reply_markup=ReplyKeyboardRemove())
    else:
        v = random.randint(0, len(bad_replies)-1)
        update.message.reply_text(bad_replies[v])

def get_value(update, context):
    key = update.message.chat.id
    try:
        value = int(context.user_data[key])
        return value
    except KeyError:
        value = 3
        return value
    
def recent_vids(update, context):
	text = "Recent Searches:\n"
	for i in range (len(q)-1, -1, -1):
		text = text + "{}.  ".format(len(q)-i) + q[i] + "\n"
	update.message.reply_text(text)

def write_links(update, url, text):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "lxml")
    links = soup.find_all('a', class_ = "js-mxp")
    val = 40
    if len(links) < val:
        val = len(links)
    for i in range (0, val, 2):
        x = links[i]['data-mxptext']
        y = re.sub(r"\s+", '_', x) 
        text = text + "{}.  /".format((i+3)//2) + y + "\n"
    update.message.reply_text(text)
    
def trending(update, context):
    text = "Trending List:\n"
    url = "https://www.pornhub.com/pornstars?o=t"
    write_links(update, url, text)
    
def most_viewed(update, context):
    text = "Most Viewed List:\n"
    url = "https://www.pornhub.com/pornstars?o=mv"
    write_links(update, url, text)
    
def most_subscribed(update, context):
    text = "Most Subscribed List:\n"
    url = "https://www.pornhub.com/pornstars?o=ms"
    write_links(update, url, text)
    
def echo(update, context):
    if update.message.text.startswith("/"):
        update.message.text = update.message.text[1:]
    
    mess = re.sub(r"\s+", '+', update.message.text)
    source = requests.get(url + mess)
    soup = BeautifulSoup(source.text, "lxml")
    update.message.reply_text("huuu, Showing results for {}...".format(update.message.text))
    links=soup.find_all('a', href=True)
    s=[]
    startIndex=0
    
    for x in range(0, len(links)):
        if links[x]['href'].startswith("/view_video"):
            if "https://www.pornhub.com" + links[x]['href'] not in s:
                s.append("https://www.pornhub.com" + links[x]['href'])
            if "pkey" in links[x]['href']:
                startIndex=s.index("https://www.pornhub.com"+links[x]['href'])

    s=s[startIndex+1:]
    random.shuffle(s)
    
    value = get_value(update, context)
    
    if value > len(s):
        value = len(s)
    for x in range(0, value):
        update.message.reply_text(s[x])
        
    mess2 = re.sub(r"\s+", '_', update.message.text)
    mess2 = mess2.lower()
    if "/" + mess2 not in q:   
        q.append("/" + mess2)
        q.popleft()

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = "1384259183:AAGBxjrGWMrQoFusbTRBIpXfMGlrSUxoGv4"
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("recent", recent_vids))
    dp.add_handler(CommandHandler("vids", vids))
    dp.add_handler(CommandHandler("trending", trending))
    dp.add_handler(CommandHandler("viewed", most_viewed))
    dp.add_handler(CommandHandler("subscribed", most_subscribed))
    dp.add_handler(MessageHandler(Filters.regex('^[0-9]+$'), set_vids))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.regex('^[0-9]+$'), echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()