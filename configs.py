from pyrogram import Client
import argparse
from os import remove

parser = argparse.ArgumentParser()
parser.add_argument('-i','--api_id')
parser.add_argument('-s','--api_hash')
parser.add_argument('-b','--bot_token')
options = parser.parse_args()

api_id = options.api_id
api_hash = options.api_hash

def ensure_connection(client_name):

    if client_name == "user":
        try:
            useraccount = Client(
                "user", api_id, api_hash
            )
            useraccount.start();return useraccount
        except:
            remove('user.session');print("\nError. Try again.\n")
    if client_name == "bot":
        try:
            bot_token = options.bot_token
            bot = Client(
                "bot", api_id, api_hash, bot_token=bot_token
            )
            bot.start();return bot
        except:
            remove('bot.session');print("\nError. Try again.\n")

useraccount = ensure_connection("user")
if options.bot_token != 'blank':
    bot = ensure_connection("bot")
    BOT_TOKEN=options.bot_token
    BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
    bot_id=f'bot_id:{BOT_ID}'
else: bot_id=''

data=f"""\
[default]
{bot_id}
user_delay_seconds:10
bot_delay_seconds:1.2
skip_delay_seconds:1\
"""
with open('config.ini', 'w') as f:
    f.write(data)