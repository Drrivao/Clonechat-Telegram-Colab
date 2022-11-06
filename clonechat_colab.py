import json, os, time
from configparser import ConfigParser
from pyrogram import Client
from pyrogram.errors import (
	FloodWait,TakeoutInitDelay
)
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import ChatPrivileges
from argparse import ArgumentParser

def config_data():
	
	config_data = ConfigParser()
	config_data.read("config.ini")
	config_data = dict(config_data["default"])

	USER_DELAY_SECONDS = float(config_data["user_delay_seconds"])
	BOT_DELAY_SECONDS = float(config_data["bot_delay_seconds"])
	SKIP_DELAY_SECONDS = float(config_data["skip_delay_seconds"])
	BOT_ID=config_data["bot_id"]

	values={
		"USER_DELAY_SECONDS":USER_DELAY_SECONDS,
		"BOT_DELAY_SECONDS":BOT_DELAY_SECONDS,
		"SKIP_DELAY_SECONDS":SKIP_DELAY_SECONDS,
		"BOT_ID":BOT_ID,
	}
	return values

def ensure_connection(client_name):

	if client_name == "user":
		useraccount = Client(client_name)
		useraccount.start()
		return useraccount

	if client_name == "bot":
		bot = Client(client_name)
		bot.start()
		return bot

def get_chats(client):

	global channel_origem
	global destino
	global chat_ids

	names_ch = []
	ids_ch = []
	list_ch = client.get_dialogs()

	for dialog in list_ch:

		channels_names = str(dialog.chat.title or dialog.chat.first_name)
		channels_ids = int(dialog.chat.id)
		names_ch.append(channels_names)
		ids_ch.append(channels_ids)

	channel_origem=names_ch.index(ORIG)
	origin_chat = ids_ch[channel_origem]
	chat_ids=get_valid_ids(client,origin_chat)

	if DEST=='auto':
		channel_destino = client.create_channel(title=f'{names_ch[channel_origem]}-clone')
		destino = channel_destino.id
	else:
		channel_destino=names_ch.index(DEST)
		destino = ids_ch[channel_destino]

	if MODE == "bot":
		chats=[origin_chat,destino]
		for chat in chats:
			client.promote_chat_member(
				chat,config_data()["BOT_ID"],
				ChatPrivileges(can_post_messages=True)
			)

	return origin_chat

def foward_photo(message, destino):

	caption = get_caption(message)
	photo_id = message.photo.file_id
	try:
		tg.send_photo(
			chat_id=destino,
			photo=photo_id,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_photo(message, destino)

def foward_text(message, destino):

	text = message.text
	try:
		tg.send_message(
			chat_id=destino,
			text=text,
			disable_notification=True,
			disable_web_page_preview=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_text(message, destino)

def foward_sticker(message, destino):

	sticker_id = message.sticker.file_id
	try:
		tg.send_sticker(chat_id=destino, sticker=sticker_id)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_sticker(message, destino)

def foward_document(message, destino):

	caption = get_caption(message)
	document_id = message.document.file_id
	try:
		tg.send_document(
			chat_id=destino,
			document=document_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_document(message, destino)

def foward_animation(message, destino):

	caption = get_caption(message)
	animation_id = message.animation.file_id
	try:
		tg.send_animation(
			chat_id=destino,
			animation=animation_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_animation(message, destino)

def foward_audio(message, destino):

	caption = get_caption(message)
	audio_id = message.audio.file_id
	try:
		tg.send_audio(
			chat_id=destino,
			audio=audio_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_audio(message, destino)

def foward_voice(message, destino):

	caption = get_caption(message)
	voice_id = message.voice.file_id
	try:
		tg.send_voice(
			chat_id=destino,
			voice=voice_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_voice(message, destino)

def foward_video_note(message, destino):

	video_note_id = message.video_note.file_id
	try:
		tg.send_video_note(
			chat_id=destino,
			video_note=video_note_id,
			disable_notification=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_video_note(message, destino)

def foward_video(message, destino):

	caption = get_caption(message)
	video_id = message.video.file_id
	try:
		tg.send_video(
			chat_id=destino,
			video=video_id,
			disable_notification=True,
			caption=caption,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_video(message, destino)

def foward_poll(message, destino):

	if message.poll.type != "regular":
		return
	try:
		tg.send_poll(
			chat_id=destino,
			question=message.poll.question,
			options=[option.text for option in message.poll.options],
			is_anonymous=message.poll.is_anonymous,
			allows_multiple_answers=message.poll.allows_multiple_answers,
			disable_notification=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_poll(message, destino)

def get_caption(message):

	if message.caption:
		caption = message.caption if premium\
		is True else message.caption[:1024]
	else:
		caption = None
	return caption

def get_sender(message):

	if message.photo:
		return foward_photo
	if message.text:
		return foward_text
	if message.document:
		return foward_document
	if message.sticker:
		return foward_sticker
	if message.animation:
		return foward_animation
	if message.audio:
		return foward_audio
	if message.voice:
		return foward_voice
	if message.video:
		return foward_video
	if message.video_note:
		return foward_video_note
	if message.poll:
		return foward_poll

	print("\nNot recognized message type:\n")
	print(message)
	raise Exception

def get_files_type_excluded_by_input(input_string):

	files_type_excluded = []
	if input_string == "all types" or "0" in input_string:
		return files_type_excluded
	else:
		if "photo" not in input_string:
			files_type_excluded += [foward_photo]
		if "text" not in input_string:
			files_type_excluded += [foward_text]
		if "document" not in input_string:
			files_type_excluded += [foward_document]
		if "sticker" not in input_string:
			files_type_excluded += [foward_sticker]
		if "animation" not in input_string:
			files_type_excluded += [foward_animation]
		if "audio" not in input_string:
			files_type_excluded += [foward_audio]
		if "voice" not in input_string:
			files_type_excluded += [foward_voice]
		if "video" not in input_string:
			files_type_excluded += [foward_video]
		if "poll" not in input_string:
			files_type_excluded += [foward_poll]
		if len(files_type_excluded) == 9:
			print("Invalid option! Try again")
			return get_files_type_excluded_by_input(input_string)
			
	return files_type_excluded

def get_message(origin_chat, message_id):

	try:
		message = tg.get_messages(origin_chat, message_id)
		return message
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	return get_message(origin_chat, message_id)

def get_list_posted(CACHE_FILE,int_task_type):

	if int_task_type == 1:
		if os.path.exists(CACHE_FILE):
			os.remove(CACHE_FILE)
		return []
	else:
		if os.path.exists(CACHE_FILE):
			with open(CACHE_FILE, mode="r") as file:
				posted = json.loads(file.read())
				return posted
		else:
			return []

def wait_a_moment(skip=False):

	if skip:
		time.sleep(
			config_data()["SKIP_DELAY_SECONDS"]
		)
	else:
		time.sleep(DELAY_AMOUNT)

def update_cache(CACHE_FILE, list_posted):

	with open(CACHE_FILE, mode="w") as file:
		file.write(json.dumps(list_posted))

def get_valid_ids(client,origin_chat):

	chat_ids=[]
	print('Getting messages...')

	if QUERY == 'all':
		hist=client.get_chat_history(origin_chat)
		for message in hist:
			if message.media or message.text or message.poll:
				chat_ids.append(message.id)
	else:
		sch=client.search_messages(origin_chat, query=QUERY)
		for message in sch:
			chat_ids.append(message.id)

	chat_ids.sort()
	return chat_ids

def must_be_ignored(
	func_sender,FILES_TYPE_EXCLUDED,curr, last
) -> bool:

	if func_sender in FILES_TYPE_EXCLUDED:
		print(f"{curr}/{last} (skip by type)")
		wait_a_moment(skip=True)
		return True
	else:
		return False

def ensure_folder_existence(folder_path):

	if not os.path.exists(folder_path):
		os.mkdir(folder_path)

def get_task_file(ORIGIN_CHAT_TITLE, destino):

	ensure_folder_existence("posteds")
	ensure_folder_existence(os.path.join("posteds"))
	task_file_name = f"{ORIGIN_CHAT_TITLE}-{destino}.json"
	task_file_path = os.path.join("posteds", task_file_name)

	return task_file_path

def main(origin_chat):

	FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input(TYPE)
	CACHE_FILE = get_task_file(ORIG, destino)

	int_task_type = NEW
	list_posted = get_list_posted(CACHE_FILE,int_task_type)
	ids_to_try=chat_ids[len(list_posted):]
	if LIMIT != 0: ids_to_try=ids_to_try[:LIMIT]
	last=len(ids_to_try)

	for message_id in ids_to_try:

		curr=ids_to_try.index(message_id)+1
		message = get_message(origin_chat, message_id)
		func_sender = get_sender(message)

		if must_be_ignored(
			func_sender,FILES_TYPE_EXCLUDED, curr, last
		):
			list_posted += [message.id]
			update_cache(CACHE_FILE, list_posted)
			continue

		func_sender(message, destino)
		print(f"{curr}/{last}")
		list_posted += [message.id]
		update_cache(CACHE_FILE, list_posted)

		if curr!=last:
			wait_a_moment()

	print('Task completed!')
	tg.stop()

def start():

	global DELAY_AMOUNT
	global premium,tg

	try:
		client=Client('user',takeout=True)
		with client:
			origin_chat_id=get_chats(client)

		os.system("clear||cls")
		useraccount = ensure_connection("user")
		premium=useraccount.get_users('me').is_premium

		if MODE == "bot":
			bot = ensure_connection("bot")
			bot.set_parse_mode(ParseMode.DISABLED)
			tg = bot
			DELAY_AMOUNT = config_data()["BOT_DELAY_SECONDS"]
		else:
			useraccount.set_parse_mode(ParseMode.DISABLED)
			tg = useraccount
			DELAY_AMOUNT = config_data()["USER_DELAY_SECONDS"]
		main(origin_chat_id)

	except TakeoutInitDelay:
		print('Confirm the data export request first.');exit()
	except Exception as e:
		print(f"It wasn't possible to continue due to {e}\n");exit()

def connect_to_api(API_ID,API_HASH,BOT_TOKEN):

	os.system("clear||cls")
	try:
		useraccount = Client(
			"user", API_ID, API_HASH
		)
		with useraccount:
			useraccount.send_message(
				"me", "Message sent with **Pyrogram**!"
			)
			user_id=useraccount.get_users('me').id
	except Exception as e:
		os.remove('user.session')
		print(f"Connection failed due to {e}.")

	if BOT_TOKEN != 'blank':
		try:
			bot = Client(
				"bot", API_ID, API_HASH,
				bot_token=BOT_TOKEN
			)
			with bot:
				bot.send_message(
					user_id, "Message sent with **Pyrogram**!"
				)
			BOT_ID=BOT_TOKEN[:BOT_TOKEN.find(':')]
			BOT_ID=f'bot_id:{BOT_ID}'
		except Exception as e:
			os.remove('bot.session')
			print(f"Connection failed due to {e}.")
	else: BOT_ID=''

	data=f"[default]\n{BOT_ID}\nuser_delay_seconds:10\n"+\
	"bot_delay_seconds:1.2\nskip_delay_seconds:1"
	
	with open('config.ini', 'w') as f:
		f.write(data)

parser = ArgumentParser()
parser.add_argument("-o","--orig", type=str)
parser.add_argument("-d","--dest", type=str)
parser.add_argument('--auth', action='store_true')
parser.add_argument('--no-auth', dest='auth', action='store_false')
parser.set_defaults(auth=True)
parser.add_argument("-m","--mode",choices=["user", "bot"])
parser.add_argument("-q","--query", type=str)
parser.add_argument("-n","--new", type=int, choices=[1, 2])
parser.add_argument("-l","--limit", type=int)
parser.add_argument("-t","--type", type=str)
parser.add_argument('-i','--api-id', type=int)
parser.add_argument('-s','--api-hash', type=str)
parser.add_argument('-b','--bot-token', type=str)
options = parser.parse_args()

ORIG = options.orig
DEST = options.dest
MODE = options.mode
NEW = options.new
LIMIT=options.limit
QUERY=options.query
TYPE = options.type

if __name__=="__main__":

	if options.auth:
		connect_to_api(
			options.api_id,
			options.api_hash,
			options.bot_token
		)
	else:
		start()