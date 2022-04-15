#!/usr/bin/env python

"""Telepathy archiving module:
    A tool for archiving Telegram chats within specific parameters.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
from telethon import functions, types
import datetime, csv, os
import details as ds
import pandas as pd

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.1"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups=[]

filetime = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")
filetime_clean = str(filetime)

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    groups.append(chat)

print('Welcome to the Telepathy archiving tool. This tool will archive Telegram chats based on a list.')
if inputFile == "":
    inputFile = "to_archive.csv"

if batch:
    user_selection_log = "n"
    user_selection_media = "n"
else:
    user_selection_log = input('Do you want to print messages to terminal while Telepathy runs? (y/n)')
    user_selection_media = input('Do you want to archive media content? (y/n)')

print('Archiving chats...')

async def main():
    toArchiveDF = pd.read_csv('../input/' + inputFile, sep=';')
    channelList = toArchiveDF.To.unique()
    for channel in channelList:
        print("Working on ",channel," This may take a while...")
        if batch:
            channelDF = toArchiveDF[toArchiveDF['To'] == channel]
            if(len(channelDF.index) == 1 ):
                user_selection_media = channelDF['Media'].values[0]
            elif(len(channelDF.index) > 0 ):
                print(f"WARNING: '{channel}' appears more than once in {inputfile}! Using first value.")
                user_selection_media = channelDF['Media'].values[0]
            else:
                print("No valid 'media' value for {channel}. Using default (no)")
                user_selection_media = "n"
        if (not pd.isna(channelDF['Startdate'].values[0]) and len(channelDF['Startdate'].values[0]) == 10):
            d_start = datetime.datetime.strptime(channelDF['Startdate'].values[0], '%Y-%m-%d')
        else:
            d_start = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
        if (not pd.isna(channelDF['Enddate'].values[0]) and len(channelDF['Enddate'].values[0]) == 10):
            d_end = datetime.datetime.strptime(channelDF['Enddate'].values[0], '%Y-%m-%d')
        else:
            d_end = datetime.datetime.strptime('2037-01-01', '%Y-%m-%d')

        l = []
        try:
            channel_clean = channel
            alphanumeric = ""

            for character in channel_clean:
                if character.isalnum():
                    alphanumeric += character
            if len(outputSubfolder) != 0:
                directory = '../output/' + outputSubfolder + '/archive/' + alphanumeric
            else:
                directory = '../output/archive/' + alphanumeric

            try:
                os.makedirs(directory)
            except FileExistsError:
                pass
            media_directory = directory + '/media'

            try:
                os.makedirs(media_directory)
            except FileExistsError:
                pass

            async for message in client.iter_messages(channel, reverse = True, offset_date = d_start):
                if message is not None:
                    try:
                        if message.sender is None:
                            authorName = ""
                            authorID = ""
                            authorUsername = ""
                        else:
                            authorName = get_display_name(message.sender)
                            authorID = message.sender.id
                            authorUsername = message.sender.username
                        year = str(format(message.date.year, '02d'))
                        month = str(format(message.date.month, '02d'))
                        day = str(format(message.date.day, '02d'))
                        hour = str(format(message.date.hour, '02d'))
                        minute = str(format(message.date.minute, '02d'))
                        if message.reply_to_msg_id is None:
                            reply = ""
                        else:
                            reply = int(message.reply_to_msg_id)
                        if message.text is None:
                            message.text = ""
                        if message.views is None:
                            views = ""
                        else:
                            views = int(message.views)
                        if message.fwd_from is None or message.fwd_from.from_id is None:
                            forward_ID = ""
                            forward_name = ""
                            forward_username = ""
                            forward_post_ID = ""
                            forward_author = ""
                        else:
                            ent = await client.get_entity(message.fwd_from.from_id)
                            forward_ID = ent.id
                            if(hasattr(ent, 'title')):
                                forward_name = ent.title
                            else:
                                forward_name = ""
                            forward_username = ent.username
                            if message.fwd_from.channel_post is None:
                                forward_post_ID = ""
                            else:
                                forward_post_ID = int(message.fwd_from.channel_post)
                            forward_author = message.fwd_from.post_author

                        date = year + "-" + month + "-" + day
                        time = hour + ":" + minute
                        timestamp = date + ', ' + time

                        if user_selection_log == 'y':
                            print(authorName,':','"' + message.text + '"',timestamp)
                        else:
                            pass
                        
                        datestamp = year + "," + month + "," + day
                        datestamp_clean = datetime.datetime.strptime(datestamp, '%Y,%m,%d')
                        timestamp = year + "-" + month + "-" + day + ", " + hour + ":" + minute

                        if d_start <= datestamp_clean and d_end >= datestamp_clean:
                            path = ""
                            if user_selection_media == 'y':
                                if message.media:
                                    try:
                                        path = await message.download_media(file=media_directory)
                                    except Exception as e:
                                        print(e)
                                    if user_selection_log == 'y':
                                        print('File saved to', path)
                                else:
                                    pass
                            l.append([channel,message.id,authorName,authorID, authorUsername, message.text, timestamp,reply,views,forward_ID,forward_name,forward_username,forward_author,forward_post_ID,path])
                    except Exception as e:
                        print(e)
                        continue
                else:
                    l.append(['None','None','None','None','None','None','None','None','None','None','None','None', 'None', 'None','None','None'])
                    continue
        
            channelArchiveDF = pd.DataFrame(l, columns = ['Chat name','message ID','Author Name','Author ID','Author Username','Message text','Timestamp','Reply to','Views','Forward Peer ID','Forwarded From','Forwarded From Username', 'Forwarded From Authorname','Forward post ID', 'MediaPath'])

            file = directory + '/'+ alphanumeric + '_' + filetime_clean +'_archive.csv'

            with open(file, 'w+') as f:
                channelArchiveDF.to_csv(f, sep=';')



            jsons = directory + '/' + 'json_files'
            try:
                os.makedirs(jsons)
            except FileExistsError:
                pass

            channelArchiveDF.to_json(jsons+'/'+alphanumeric+'_archive.json',orient='split',compression='infer',index='true')

            print("Scrape completed for",channel,", file saved")

            channelArchiveDF = pd.DataFrame(None)

        except Exception as e:
            print("An exception occurred.", e)

with client:
    client.loop.run_until_complete(main())

print('List archived successfully')

if batch:
    again = "n"
else:
    again = input('Do you want to archive more groups? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("archiver.py").read())
else:
    pass

if batch:
    launcher = "n"
else:
    launcher = input('Do you want to return to the launcher? (y/n)')
if launcher == 'y':
    print('Restarting...')
    exec(open("telepathy.py").read())
else:
    print('Thank you for using Telepathy.')
