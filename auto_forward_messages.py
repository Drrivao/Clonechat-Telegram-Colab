"""Auto Forward Messages"""
from argparse import ArgumentParser,BooleanOptionalAction
from pyrogram.errors import MessageIdInvalid
from pyrogram.enums import ParseMode
from pyrogram.types import ChatPrivileges
from configparser import ConfigParser
from pyrogram import Client
import time
import json
import os
import re

def is_chat_id(chat):
	chat=re.match(r'^(-100)\d{10}|(^\d{10})',chat)
	return chat is not None

def get_chats(client,bot_id):
	chat=client.get_chat(int(from_chat)) if is_chat_id(from_chat)\
	else client.get_chat(str(from_chat))
	name=f"{chat.first_name} {chat.last_name}"
	chat_title=chat.title
	chats["from_chat_id"]=chat.id
	from_chat_title=chat_title if chat_title else name

	if to_chat:
		chats["to_chat_id"]=int(to_chat) if is_chat_id(to_chat)\
		else client.get_chat(str(to_chat)).id
	else:
		dest = client.create_channel(
			title=f'{from_chat_title}-clone'
		)
		chats["to_chat_id"]=dest.id

	if mode == "bot":
		for chat in [
			chats["from_chat_id"],chats["to_chat_id"]
		]:
			client.promote_chat_member(
				privileges=ChatPrivileges(
				can_post_messages=True),
				chat_id=chat,
				user_id=bot_id
			)

def connect_to_api(api_id,api_hash,bot_token):
	client=Client('user',api_id=api_id,api_hash=api_hash)
	with client:
		user_id=client.get_users('me').id
		client.send_message(
			user_id,"Message sent with **Auto Forward Messages**!"
		)
	if bot_token:
		client=Client(
			'bot',api_id=api_id,api_hash=api_hash,bot_token=bot_token
		)
		bot_id=bot_token[:bot_token.find(':')]
		bot_id=f'bot_id:{bot_id}'
		with client:
			client.send_message(
				user_id,"Message sent with **Auto Forward Messages**!"
			)
	else:
		bot_id='bot_id:none'

	data=f"[default]\n{bot_id}\nuser_delay_seconds:10"+\
	"\nbot_delay_seconds:5"
	with open('config.ini', 'w') as f:
		f.write(data)
	return client

def is_empty_message(message) -> bool:
    if message.empty or message.service or message.dice or message.location:
        return True

def filter_messages(client):
	list_ids=[]
	print("Getting messages...\n")
	if query == "":
		messages=client.get_chat_history(chats["from_chat_id"])
		messages=[msg for msg in messages if not is_empty_message(msg)]
	else:
		messages=client.search_messages(
			chats["from_chat_id"], query=query
		)
	if filter:
		for message in messages:
			if message.media:
				msg_media=str(message.media)
				msg_type=msg_media.replace('MessageMediaType.','')
				if msg_type.lower() in filter:
					list_ids.append(message.id)
			if message.text and "text" in filter:
				list_ids.append(message.id)
			if message.poll and "poll" in filter:
				list_ids.append(message.id)
	else:
		list_ids=[message.id for message in messages]

	return list_ids

def get_ids(client):
	global CACHE_FILE
	total=client.get_chat_history_count(chats["from_chat_id"])
	if total > 25000:
		print(
			"Warning: The origin chat contains a large number of messages.\n"+
			"It is recommended to forward up to 1000 messages per day.\n"
		)

	chat_hist=filter_messages(client)
	chat_hist.sort()
	cache =f'{chats["from_chat_id"]}_{chats["to_chat_id"]}.json'
	CACHE_FILE=f'posteds/{cache}'

	if options.resume and os.path.exists(CACHE_FILE):
		with open(CACHE_FILE,"r") as j:
			forwarded = json.load(j)
		chat_ids=[
			msg_id for msg_id in chat_hist\
			if msg_id not in forwarded
		]
	else:
		forwarded=[]
		chat_ids=chat_hist
	if limit != 0:
		chat_ids=chat_ids[:limit]

	return chat_ids,forwarded

def auto_forward(client,chat_ids,forwarded):
	os.makedirs('posteds',exist_ok=True)
	for message_id in chat_ids:
		try:
			os.system('clear || cls')
			print(f"Forwarding: {chat_ids.index(message_id)+1}/{len(chat_ids)}")
			client.forward_messages(
				from_chat_id=chats["from_chat_id"],
				chat_id=chats["to_chat_id"],
				message_ids=message_id
			)
			with open(CACHE_FILE,"w") as j:
				json.dump(forwarded+chat_ids[:chat_ids.index(message_id)+1],j)
			if message_id != chat_ids[-1]:
				time.sleep(delay)
		except MessageIdInvalid:
			pass
	print("\nTask completed!\n")

def countdown():
	time_sec = 4*3600
	while time_sec:
		mins, secs = divmod(time_sec, 60)
		hours, mins = divmod(mins, 60)
		timeformat = f'{hours:02d}:{mins:02d}:{secs:02d}'
		print('Restarting in:',timeformat, end='\r')
		time.sleep(1)
		time_sec -= 1

def get_full_chat():
	client=Client('user',takeout=True)
	with client:
		get_chats(client,configs["bot_id"])
		chat_ids,forwarded=get_ids(client)
	app=Client(mode)
	app.set_parse_mode(ParseMode.DISABLED)
	with app:
		auto_forward(app,chat_ids,forwarded)

def main():
	global delay
	if options.api_id:
		connect_to_api(options.api_id,options.api_hash,options.bot_token)
	else:
		config_data = ConfigParser()
		config_data.read("config.ini")
		config_data = dict(config_data["default"])
		configs["user_delay_seconds"]=float(config_data["user_delay_seconds"])
		configs["bot_delay_seconds"]=float(config_data["bot_delay_seconds"])
		configs["bot_id"]=config_data["bot_id"]

		delay=configs["user_delay_seconds"] if mode == "user"\
		else configs["bot_delay_seconds"]

		if options.restart:
			while True:
				get_full_chat()
				countdown()
		else:
			get_full_chat()

os.system('clear || cls')
parser = ArgumentParser()
parser.add_argument(
	"-m","--mode",choices=["user", "bot"],default="user",
	help="'user'=forward in user mode,'bot'=forward in bot mode"
)
parser.add_argument(
	"-R","--restart", action=BooleanOptionalAction,
	help="The program will restart searching for new messages on origin chat."
)
parser.add_argument("-o","--orig",help="Origin chat id")
parser.add_argument("-d","--dest",help="Destination chat id")
parser.add_argument("-q","--query",type=str,default="",help="Query sting")
parser.add_argument("-r","--resume", action=BooleanOptionalAction,help="Resume task")
parser.add_argument("-l","--limit",type=int,default=0,help="Max number of messages to forward")
parser.add_argument("-f","--filter",type=str,default=None,help="Filter messages by kind")
parser.add_argument('-i','--api-id',type=int,help="Api id")
parser.add_argument('-s','--api-hash',type=str,help="Api hash")
parser.add_argument('-b','--bot-token',type=str,help="Token of a bot")
options = parser.parse_args()

configs={}
chats={}

from_chat=options.orig
to_chat=options.dest
mode=options.mode
query=options.query
limit=options.limit
filter = options.filter
filter=filter.split(",") if\
filter else None

if __name__=="__main__":
	main()