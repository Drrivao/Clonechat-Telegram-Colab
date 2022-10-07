from configparser import ConfigParser
from pyrogram import Client
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('--api_id')
parser.add_argument('--api_hash')
parser.add_argument('--bot_token')
options = parser.parse_args()

def config_vars(i,j):

    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as f:
            f.write('[default]')

    config = ConfigParser()
    config.read('config.ini')
    config.set('default',i,j)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def ensure_connection(client_name):

    if client_name == "user":
        while True:
            try:
                api_id = options.api_id
                api_hash = options.api_hash

                useraccount = Client("user", api_id, api_hash)
                useraccount.start()
                return useraccount
            except:
                print("\nError. Try again.\n")
                pass
    else:
        pass

    if client_name == "bot":
        while True:
            try:
                api_id = options.api_id
                api_hash = options.api_hash
                bot_token = options.bot_token

                bot = Client(
                    client_name, api_id, api_hash, bot_token=bot_token
                )
                bot.start()
                return bot
            except:
                print("\nError. Try again.\n")
                pass

useraccount = ensure_connection("user")
if options.bot_token != 'blank':
    bot = ensure_connection("bot")
    BOT_TOKEN=options.bot_token
    BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
else: BOT_ID=''

vars={
    'bot_id':BOT_ID,
    'user_delay_seconds':'25',
    'bot_delay_seconds':'1.2',
    'skip_delay_seconds':'1'
}

k=list(vars.keys())
v=list(vars.values())

for n in range(len(vars)):
    config_vars(k[n],v[n])