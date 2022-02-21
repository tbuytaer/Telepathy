#!/usr/bin/env python

"""Telepathy forward scraping module:
    A tool for creating an edgelist of forwarded messages.
"""

from telethon import TelegramClient
from telethon import utils
import pandas as pd
import details as ds
import os

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

print('Welcome to channel forward scraper.\nThis tool will scrape a Telegram channel for all forwarded messages and their original sources.')


async def main(channelUsername):
    l = []
    async for message in client.iter_messages(channelUsername):

        if message.forward is not None:
            try:
                id = message.forward.original_fwd.from_id
                if id is not None:
                    ent = await client.get_entity(id)
                    if(hasattr(ent, 'title')):
                        nameID = message.from_id
                        year = format(message.date.year, '02d')
                        month = format(message.date.month, '02d')
                        day = format(message.date.day, '02d')
                        hour = format(message.date.hour, '02d')
                        minute = format(message.date.minute, '02d')

                        date = str(year) + "/" + str(month) + "/" + str(day)
                        time = str(hour) + ":" + str(minute)
                        timestamp = date + ", " + time
                        if user_selection_log == 'y':
                            print(ent.title,">>>",channelUsername)
                        else:
                            pass

                        l.append([channelUsername, ent.id, ent.title, ent.username, timestamp])

            except:
                if user_selection_log == 'y':
                    print("An exception occurred: Could be private, now deleted, or a group.")
                else:
                    pass

    name_clean = channelUsername
    alphanumeric = ""

    for character in name_clean:
        if character.isalnum():
            alphanumeric += character

    if len(subfolder) != 0:
        directory = './output/' + subfolder + '/' + 'edgelists/'
    else:
        directory = './output/edgelists/'
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    channelForwardDF = pd.DataFrame(l, columns = ['To', 'FromID', 'FromName', 'FromUsername', 'timestamp'])

    file = directory + alphanumeric + '_edgelist.csv'

    with open(file,'w+') as f:
        channelForwardDF.to_csv(f)



if batch:
    user_selection_log = "n"
    toForwardDF = pd.read_csv('forwardchannels.csv')
    channelList = toForwardDF.Username.unique()

    for channelUsername in channelList:
        print('Scraping forwards from', channelUsername, 'This may take a while...')
        with client:
            client.loop.run_until_complete(main(channelUsername))
else:
    user_selection_log = input('Do you want to print forwards to terminal while Telepathy runs? (y/n)')
    while True:
        try:
            channelUsername = input("Please enter a Telegram channel name:\n")
            print(f'You entered "{channelUsername}"')
            answer = input('Is this correct? (y/n)')
            if answer == 'y':
                print('Scraping forwards from', channelUsername, 'This may take a while...')
                break;
        except:
                continue
    with client:
            client.loop.run_until_complete(main(channelUsername))


print('Forwards scraped successfully.')

if batch:
    next1 = "n"
else:
    next1 = input('Do you also want to scrape forwards from the discovered channels? (y/n)')
if next1 == 'y':
    print('Scraping forwards from channels discovered in', channelUsername, '...')
    async def new_main():
        name_clean = channelUsername
        alphanumeric = ""

        for character in name_clean:
            if character.isalnum():
                alphanumeric += character
        df = pd.read_csv('./output/' + subfolder + '/' + 'edgelists/'+ alphanumeric + '_edgelist.csv')
        df = df.FromUsername.unique()
        l = []
        for i in df:
            async for message in client.iter_messages(i):
                if message.forward is not None:
                    try:
                        id = message.forward.original_fwd.from_id
                        if id is not None:
                            ent = await client.get_entity(id)
                            year = format(message.date.year, '02d')
                            month = format(message.date.month, '02d')
                            day = format(message.date.day, '02d')
                            hour = format(message.date.hour, '02d')
                            minute = format(message.date.minute, '02d')

                            date = str(year) + "/" + str(month) + "/" + str(day)
                            time = str(hour) + ":" + str(minute)
                            timestamp = date + ", " + time

                            if user_selection_log == 'y':
                                print(ent.title,">>>",i)
                            else:
                                pass

                            df = pd.DataFrame(l, columns = ['To', 'FromID', 'From', 'FromUsername', 'Timestamp'])

                            name_clean = channelUsername
                            alphanumeric = ""

                            for character in name_clean:
                                if character.isalnum():
                                    alphanumeric += character

                            if len(subfolder) != 0:
                                directory = './output/' + subfolder + '/' + 'edgelists/'
                            else:
                                directory = './output/edgelists/'
                            try:
                                os.makedirs(directory)
                            except FileExistsError:
                                pass

                            file1 = directory + alphanumeric + '_net.csv'

                            with open(file1,'w+') as f:
                                df.to_csv(f)

                            l.append([i, ent.id, ent.title, ent.username, timestamp])
                    except:
                        if user_selection_log == 'y':
                            print("An exception occurred: Could be private, now deleted, or a group.")
                        else:
                            pass

            print("Scrape complete for:", i,)
        df.to_json(alphanumeric + '_archive.json', orient = 'split', compression = 'infer', index = 'true')

    with client:
        client.loop.run_until_complete(new_main())
    print('Forwards scraped successfully.')
else:
    pass

if batch:
    again = "n"
else:
    again = input('Do you want to scrape more chats? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("forwards.py").read())
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
