from pyrogram import Client
import argparse
from os import remove,system

parser = argparse.ArgumentParser()
parser.add_argument('-i','--api_id')
parser.add_argument('-s','--api_hash')
parser.add_argument('-b','--bot_token')
options = parser.parse_args()

API_ID = options.api_id
API_HASH = options.api_hash
BOT_TOKEN=options.bot_token

def ensure_connection(client_name):
    if client_name == "user":
        try:
            useraccount = Client(
                "user", API_ID, API_HASH
            )
            useraccount.start()
            return useraccount
        except Exception as e:
            remove('user.session')
            print(f"Connection failed due to {e}.")
    if client_name == "bot":
        try:
            bot = Client(
                "bot", API_ID, API_HASH,
                bot_token=BOT_TOKEN
            )
            bot.start()
            return bot
        except Exception as e:
            remove('bot.session')
            print(f"Connection failed due to {e}.")

system('clear||cls')
useraccount = ensure_connection("user")

if BOT_TOKEN != 'blank':
    bot = ensure_connection("bot")
    BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
    BOT_ID=f'bot_id:{BOT_ID}'
else: BOT_ID=''

data=f"""\
[default]
{BOT_ID}
user_delay_seconds:10
bot_delay_seconds:1.2
skip_delay_seconds:1"""

with open('config.ini', 'w') as f:
    f.write(data)