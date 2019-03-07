import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

data = []

keyboard = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='View Events', callback_data='view')],
    [InlineKeyboardButton(text='Add Event', callback_data='add')],
    [InlineKeyboardButton(text='Edit Events', callback_data='edit')],
    [InlineKeyboardButton(text='About', callback_data='about')],
]) 

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, u'\U0001F4C5 Welcome to Event Management bot!\nHow may I be of help today?', reply_markup=keyboard)
    add_data(from_id, date, time, title, description)

def add_data(from_id):
    
    bot.sendMessage(from_id, text='Date of Event (MM/DD/YYYY)', parse_mode="Markdown")
        
    bot.sendMessage(from_id, text='Time of Event (i.e. 23:59)', parse_mode="Markdown")

    bot.sendMessage(from_id, text='Event Title', parse_mode="Markdown")

    bot.sendMessage(from_id, text='Event Description', parse_mode="Markdown")

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    if query_data=="view":
        if data == []:
            bot.sendMessage(from_id, text='Event list is empty. Select *Add Events* to create a new list.', parse_mode="Markdown", reply_markup=keyboard)
        else:
            bot.sendMessage(from_id, text=data)
    if query_data == "add":
        add_data(from_id)
    if query_data == "edit":
        bot.sendMessage(from_id, text='edit1')
    if query_data == "about":
        bot.sendMessage(from_id, text='about1')
    
TOKEN = '716204897:AAEV4Omttufm9BGT9x_DP-b9O8qTMI5VIwg'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
