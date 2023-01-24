"""Auto Forward Messages"""
from argparse import ArgumentParser,BooleanOptionalAction
from pyrogram.errors import FloodWait,MessageIdInvalid
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import ChatPrivileges
from configparser import ConfigParser
from pyrogram import Client,filters
import time,json,os,re

def cache():
	cache =f'{chats["from_chat_id"]}_{chats["to_chat_id"]}.json'
	CACHE_FILE=f'posteds/{cache}'
	return CACHE_FILE

def get_chats(client,bot_id):
	chat=client.get_chat(from_chat)
	name=f"{chat.first_name} {chat.last_name}"
	chat_title=chat.title
	chats["from_chat_id"]=chat.id
	from_chat_title=chat_title if chat_title is not None else name

	if to_chat is None:
		dest = client.create_channel(
			title=f'{from_chat_title}-clone'
		)
		chats["to_chat_id"]=dest.id
	else:
		chats["to_chat_id"]=client.get_chat(to_chat).id

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
	if bot_token is not None:
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
	if limit != 0:
		chat_ids=chat_ids[:limit]
	return chat_ids

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
				time.sleep(delay)
		except FloodWait as f:
			time.sleep(f.value)
		except MessageIdInvalid:
			pass
	print("Task completed!\n")

def get_configs():
	config_data = ConfigParser()
	config_data.read("config.ini")
	config_data = dict(config_data["default"])
	configs["user_delay_seconds"]=float(config_data["user_delay_seconds"])
	configs["bot_delay_seconds"]=float(config_data["bot_delay_seconds"])
	configs["bot_id"]=config_data["bot_id"]

def countdown():
	time_sec = 4*3600
	while time_sec:
		mins, secs = divmod(time_sec, 60)
		hours, mins = divmod(mins, 60)
		timeformat = f'{hours:02d}:{mins:02d}:{secs:02d}'
		print('Restarting in:',timeformat, end='\r')
		time.sleep(1)
		time_sec -= 1

def get_full_chat(delay):
	client=Client('user',takeout=True)
	with client:
		get_chats(client,configs["bot_id"])
		chat_ids=get_ids(client)
	app=Client(mode)
	app.set_parse_mode(ParseMode.DISABLED)
	with app:
		auto_forward(app,chat_ids,delay)

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
		if options.restart:
			while True:
				get_full_chat(delay)
				countdown()
		else:
			get_full_chat(delay)
	else:
		connect_to_api(
			options.api_id,
			options.api_hash,
			options.bot_token
		)