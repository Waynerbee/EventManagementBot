import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
import datetime

data = {
    'Eventname':{
        'date':'12/30/99',
        'time':'23:59',
        'desc':'This is a demo'
    }
}

userstep={
    329246276:{
        'session':'add',
        'step':0,
        'title':'eventname'
    }
}

keyboard = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='View Events', callback_data='view')],
    [InlineKeyboardButton(text='Add Event', callback_data='add')],
    [InlineKeyboardButton(text='Edit Events', callback_data='edit')],
    [InlineKeyboardButton(text='About', callback_data='about')],
]) 

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, u'\U0001F4C5 Welcome to Event Management bot!\nHow may I be of help today?', reply_markup=keyboard)
    if userstep[str(chat_id)]['session']=='add':
        schat_id=str(chat_id)
        if userstep[schat_id]['step']==0:
            data[msg['text']]={}
            userstep[schat_id]['title']=msg['text']
            userstep[schat_id]['step']+=1
            add_eventdata(chat_id,1)
        elif userstep[schat_id]['step']==1:
            dateStr = msg['text']
            date = datetime.datetime.strptime(dateStr, "%m/%d/%Y").date()
            data[userstep[schat_id]['title']]['date']=str(date)
            userstep[schat_id]['step']+=1
            add_eventdata(chat_id,2)
            
        elif userstep[schat_id]['step']==2:
            data[userstep[schat_id]['title']]['time']=msg['text']
            userstep[schat_id]['step']+=1
            add_eventdata(chat_id,3)
            
        elif userstep[schat_id]['step']==3:
            data[userstep[schat_id]['title']]['desc']=msg['text']
            userstep[schat_id]['step']+=1
            bot.sendMessage(chat_id,'Completed!')
            bot.sendMessage(chat_id, u'\U0001F680 Welcome to Event Management bot!\nHow may I be of help today?', reply_markup=keyboard)
            userstep['session']=''
            userstep['step']=0
            userstep['title']=''
        else:
            bot.sendMessage(chat_id, u'\U0001F680 Your event has been added!\nWhat would you like to do next?', reply_markup=keyboard)

def add_eventdata(from_id,step):
    # Get details of event from user
    if step==0:
        bot.sendMessage(from_id, text='Event Title',parse_mode="Markdown")
    elif step==1:
        bot.sendMessage(from_id, text='Date of Event (MM/DD/YYYY)',parse_mode="Markdown")
    elif step==2:
        bot.sendMessage(from_id, text='Time of Event (i.e. 23:59)',parse_mode="Markdown")
    elif step==3:
        bot.sendMessage(from_id, text='Event Description',parse_mode="Markdown")
    
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    if query_data=="view":
        if data == []:
            bot.sendMessage(from_id, text='Event list is empty. Select *Add Events* to create a new list.', reply_markup =keyboard)
        else:
            for  x in data:
                print (x)
                message = x + "\n" + data[x]["date"] + "\n" + data[x]["time"] + "\n" + data[x]["desc"] + "\n" + "\n"
            bot.sendMessage(from_id, text=message, reply_markup=keyboard)
    if query_data=="add":
        from_id=str(from_id)
        userstep[from_id]={}
        userstep[from_id]['session']='add'
        userstep[from_id]['step']=0
        add_eventdata(from_id,0)
    if query_data=="edit":
        bot.sendMessage(from_id, text='edit')
    if query_data=="about":
        bot.sendMessage(from_id, text='This bot chronologically sorts your events.\nCreated by @waynerbee', reply_markup=keyboard)
    
TOKEN = "<TELEGRAM TOKEN HERE>"

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

print ('Listening ...')


# Keep the program running.
while 1:
    time.sleep(1)
