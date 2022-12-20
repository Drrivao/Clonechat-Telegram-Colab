"""Auto Forward Messages"""
from pyrogram import Client,filters
from pyrogram.types import ChatPrivileges
from configparser import ConfigParser
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid
from argparse import ArgumentParser,BooleanOptionalAction
from time import sleep
from os.path import join
import os
import re
import json

def cache():
	cache =f'{chats["from_chat_id"]}_{chats["to_chat_id"]}.json'
	CACHE_FILE=join('posteds',cache)
	return CACHE_FILE

def get_chats(client,bot_id):
	dialogs = client.get_dialogs()
	if re.match(r'^(-100)|(^\d{10})',from_chat) is None:
		for dialog in dialogs:
			name=f"{dialog.chat.first_name} {dialog.chat.last_name}"
			chat_title=dialog.chat.title
			if isinstance(chat_title, str) is True:
				if from_chat == chat_title:
					chats["from_chat_id"]=dialog.chat.id
				if to_chat is not None:
					if to_chat == chat_title:
						chats["to_chat_id"]=dialog.chat.id
			if isinstance(name, str) is True:
				if from_chat == name:
					chats["from_chat_id"]=dialog.chat.id
				if to_chat is not None:
					if to_chat in name:
						chats["to_chat_id"]=dialog.chat.id
		if to_chat is None:
			dest = client.create_channel(
				title=f'{from_chat}-clone'
			)
			chats["to_chat_id"]=dest.id
	else:
		for dialog in dialogs:
			name=f"{dialog.chat.first_name} {dialog.chat.last_name}"
			chat_title=dialog.chat.title
			if from_chat in str(dialog.chat.id):
				chats["from_chat_id"]=dialog.chat.id
				from_chat_title=chat_title if chat_title\
					is not None else name
		if to_chat is None:
			dest = client.create_channel(
				title=f'{from_chat_title}-clone'
			)
			chats["to_chat_id"]=dest.id
		else:
			chats["to_chat_id"]=to_chat
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
	client=Client(
		'user',
		api_id=api_id,
		api_hash=api_hash
	)
	with client:
		user_id=client.get_users('me').id
		client.send_message(
			user_id,"Message sent with **Auto Forward Messages**!"
		)
	if bot_token is not None:
		client=Client(
			'bot',
			api_id=api_id,
			api_hash=api_hash,
			bot_token=bot_token,
		)
		bot_id=bot_token[:bot_token.find(':')]
		bot_id=f'bot_id:{bot_id}'
		with client:
			client.send_message(
				user_id,"Message sent with **Auto Forward Messages**!"
			)
	else: bot_id='bot_id:none'

	data=f"[default]\n{bot_id}\nuser_delay_seconds:10"+\
	"\nbot_delay_seconds:5"
	with open('config.ini', 'w') as f:
		f.write(data)
	return client

def filter_messages(client):
	list=[]
	print("Getting messages...\n")
	if query == "":
		messages=client.get_chat_history(chats["from_chat_id"])
	else:
		messages=client.search_messages(
			chats["from_chat_id"], query=query
		)
	for message in messages:
		if message.media:
			if filter is not None:
				msg_media=str(message.media)
				msg_type=msg_media.replace('MessageMediaType.','').lower()
				if msg_type in filter:
					list.append(message.id)
			else:
				list.append(message.id)	
		if message.text:
			if filter is not None:
				if "text" in filter:
					list.append(message.id)
			else:
				list.append(message.id)
		if message.poll:
			if filter is not None:
				if "poll" in filter:
					list.append(message.id)
			else:
				list.append(message.id)
	return list

def get_ids(client):
	total=client.get_chat_history_count(chats["from_chat_id"])
	if total > 25000:print(
	"Warning: origin chat contains a huge number of messages.\n"+
	"It's recommended forwarding up to 1000 messages a day.\n"
	)
	chat_ids=filter_messages(client)
	chat_ids.sort()
	if options.resume:
		if os.path.exists(cache()):
			with open(cache(),"r") as file:
				last_id = json.loads(file.read())
			n=chat_ids.index(last_id)+1
			chat_ids=chat_ids[n:]
	if limit != 0: chat_ids=chat_ids[:limit]
	return chat_ids

def keep_alive(delay):
	if options.keep_alive:
		print("Live mode activated")
		app=Client(mode)
		@app.on_message(
			filters.chat(chats["from_chat_id"]) #add your filters here
		)
		async def get_new_messages(client, message):
			await client.forward_messages(
				from_chat_id=chats["from_chat_id"],
				chat_id=chats["to_chat_id"],
				message_ids=message.id
			)
			with open(cache(),"w") as file:
				file.write(json.dumps(message.id))
			sleep(delay)
		app.run()

def auto_forward(client,chat_ids,delay):
	os.system('clear || cls')
	os.makedirs('posteds',exist_ok=True)
	for i in range(len(chat_ids)):
		try:
			print(f"{i+1}/{len(chat_ids)}")
			id=chat_ids[i]
			client.forward_messages(
				from_chat_id=chats["from_chat_id"],
				chat_id=chats["to_chat_id"],
				message_ids=id
			)
			with open(cache(),"w") as file:
				file.write(json.dumps(id))
			if id != chat_ids[-1:][0]:
				sleep(delay)
		except FloodWait as f:
			sleep(f.value)
		except MessageIdInvalid:
			pass
	print("Task completed!")

def get_configs():
	config_data = ConfigParser()
	config_data.read("config.ini")
	config_data = dict(config_data["default"])
	configs["user_delay_seconds"]=float(config_data["user_delay_seconds"])
	configs["bot_delay_seconds"]=float(config_data["bot_delay_seconds"])
	configs["bot_id"]=config_data["bot_id"]

def get_full_chat(delay):
	client=Client('user',takeout=True)
	with client:
		get_chats(client,configs["bot_id"])
		chat_ids=get_ids(client)
	app=Client(mode)
	app.set_parse_mode(ParseMode.DISABLED)
	with app:
		auto_forward(app,chat_ids,delay)
	if options.keep_alive:
		keep_alive(delay)

os.system('clear || cls')
parser = ArgumentParser()
parser.add_argument(
	"-m","--mode",choices=["user", "bot"],default="user",
	help="'user'=forward in user mode,'bot'=forward in bot mode"
)
parser.add_argument(
	"-k","--keep-alive", action=BooleanOptionalAction,
	help="Keep alive program and forward messages coming from origin chat."
)
parser.add_argument("-o","--orig",help="Origin chat id")
parser.add_argument("-d","--dest",help="Destination chat id")
parser.add_argument("-q","--query",type=str,default="",help="Query sting")
parser.add_argument("-r","--resume", action=BooleanOptionalAction,help="Resume task")
parser.add_argument("-l","--limit",type=int,default=0,help="Max number of messages to forward")
parser.add_argument("-f","--filter",type=str,default=None,help="Filter messages by kind")
parser.add_argument('-i','--api-id',type=int,help="api id")
parser.add_argument('-s','--api-hash',type=str,help="api hash")
parser.add_argument('-b','--bot-token',type=str,help="Token of a bot")
options = parser.parse_args()

configs={
	'user_delay_seconds':"",
	'bot_delay_seconds':"",
	'bot_id':""
}
chats={
	'from_chat_id':"",
	'to_chat_id':""
}
from_chat=options.orig
to_chat=options.dest
mode=options.mode
query=options.query
limit=options.limit
filter = options.filter
filter=filter.split(",") if\
filter is not None else None

if __name__=="__main__":
	if options.api_id is None:
		get_configs()
		delay=configs["user_delay_seconds"] if mode == "user"\
		else configs["bot_delay_seconds"]
		get_full_chat(delay)
	else:
		connect_to_api(
			options.api_id,
			options.api_hash,
			options.bot_token
		)