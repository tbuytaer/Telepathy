#!/usr/bin/env python

"""Telepathy: A Telegram OSINT toolkit that allows you to archive chats,
gather memberlists for groups, create edglists for forwarded messages and more.
"""

from telethon.sync import TelegramClient
from telethon import TelegramClient
import argparse

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.2"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

""" Get arguments from command line """
parser = argparse.ArgumentParser(description='Select mode')
parser.add_argument('--mode', default="menu", choices=['archive', 'archive-period', 'members', 'forwards','userlookup','menu'], help="The action to perform.")
parser.add_argument('--batch', dest = 'batch', action='store_true', help="Batch mode. Skip questions and don't return to menu afterwards.")
parser.set_defaults(batch=False)
args = parser.parse_args()
mode = args.mode

if mode == 'archive':
    print('Launching batch chat archiver')
    exec(open("archiver.py").read())
elif mode == 'archive-period':
    print('Launching chat archiver')
    exec(open("timeframe.py").read())
elif mode == 'members':
    print('Launching group member scraper...')
    exec(open("members.py").read())
elif mode == 'forwards':
    print('Launching channel forward scraper...')
    exec(open("forwards.py").read())
elif mode == 'userlookup':
    print('Launching Telegram user lookup...')
    exec(open("userlookup.py").read())
elif mode == 'menu':
    print('Welcome to Telepathy')
    print('Please select a function:')

    li = ['Batch chat archiver','Archive within a timeframe','Scrape group members','Scrape forwarded messages in a chat','Lookup a user ID']

    def display(li):
        for idx, tables in enumerate(li):
            print("%s. %s" % (idx+1, tables))

    def get_list(li):
        choose = int(input("\nPick a number:"))-1
        if choose < 0 or choose > (len(li)-1):
            print('Invalid Choice')
            return ''
        return li[choose]

    display(li)
    choice = (get_list(li))

    print('Loading', choice,'...')

    if choice == 'Batch chat archiver':
        print('Launching batch chat archiver')
        exec(open("archiver.py").read())
    if choice == 'Archive within a timeframe':
        print('Launching chat archiver')
        exec(open("timeframe.py").read())
    elif choice == 'Scrape group members':
        print('Launching group member scraper...')
        exec(open("members.py").read())
    elif choice == 'Scrape forwarded messages in a chat':
        print('Launching channel forward scraper...')
        exec(open("forwards.py").read())
    elif choice == 'Lookup a user ID':
        print('Launching Telegram user lookup...')
        exec(open("userlookup.py").read())
