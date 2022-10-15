import argparse, json, os, time
from configparser import ConfigParser
from pyrogram import Client
from pyrogram.errors import ChannelInvalid, FloodWait, PeerIdInvalid
from pyrogram.types import ChatPrivileges

def start():

	global CACHE_FILE
	global FILES_TYPE_EXCLUDED

	ORIGIN_CHAT_TITLE = check_chat_id(origin_chat)
	if ORIGIN_CHAT_TITLE is False:
		raise AttributeError("Fix the origin chat_id")
	FILES_TYPE_EXCLUDED = []

	DESTINATION_CHAT_TITLE = check_chat_id(origin_chat)
	if DESTINATION_CHAT_TITLE is False:
		raise AttributeError("Fix the destination chat_id")

	if options.type is None:
		pass
	else:
		TYPE = options.type
		FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input(TYPE)

	CACHE_FILE = get_task_file(ORIGIN_CHAT_TITLE, destino)
	main()

def ensure_connection(client_name):

	if client_name == "user":
		try:
			useraccount = Client(
				client_name,takeout=True
			)
			useraccount.start()
			return useraccount
		except:
			print("Delete Session file and try again.")
	else:
		pass

	if client_name == "bot":
		try:
			bot = Client(client_name)
			bot.start()
			return bot
		except:
			print("Delete Session file and try again.")

def get_chats():

	global origin_chat
	global channel_origem
	global destino

	names_ch = []
	ids_ch = []
	list_ch = useraccount.get_dialogs()

	for cod, dialog in enumerate(list_ch):
		channels_names = str(dialog.chat.title or dialog.chat.first_name)
		channels_ids = int(dialog.chat.id)
		names_ch.append(channels_names)
		ids_ch.append(channels_ids)

	channel_origem=names_ch.index(options.orig)
	origin_chat = ids_ch[channel_origem]

	if options.dest is None:
		channel_destino = useraccount.create_channel(title=f'{names_ch[channel_origem]}-clone')
		destino = channel_destino.id
	else:
		channel_destino=names_ch.index(options.dest)
		destino = ids_ch[channel_destino]

	if options.mode == "bot":
		chats=[origin_chat,destino]
		for chat in chats:
			useraccount.promote_chat_member(
				chat,BOT_ID,
				ChatPrivileges(can_post_messages=True)
			)

def get_config_data(path_file_config):
	"""get default configuration data from file config.ini
	Returns:
		dict: config data
	"""
	config_file = ConfigParser()
	config_file.read(path_file_config)
	default_config = dict(config_file["default"])
	return default_config

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

	text = message.text.markdown
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
		caption = message.caption.markdown
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
	if input_string == "" or "0" in input_string:
		return files_type_excluded
	else:
		if "1" not in input_string:
			files_type_excluded += [foward_photo]
		if "2" not in input_string:
			files_type_excluded += [foward_text]
		if "3" not in input_string:
			files_type_excluded += [foward_document]
		if "4" not in input_string:
			files_type_excluded += [foward_sticker]
		if "5" not in input_string:
			files_type_excluded += [foward_animation]
		if "6" not in input_string:
			files_type_excluded += [foward_audio]
		if "7" not in input_string:
			files_type_excluded += [foward_voice]
		if "8" not in input_string:
			files_type_excluded += [foward_video]
		if "9" not in input_string:
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

def get_list_posted(int_task_type):

	# 1 = new
	if int_task_type == 1:
		if os.path.exists(CACHE_FILE):
			os.remove(CACHE_FILE)
		return []
	else:  # 2 = resume
		if os.path.exists(CACHE_FILE):
			with open(CACHE_FILE, mode="r") as file:
				posted = json.loads(file.read())
				return posted
		else:
			return []

def wait_a_moment(message_id, skip=False):

	if message_id != 1:
		if skip:
			time.sleep(DELAY_SKIP)
		else:
			time.sleep(DELAY_AMOUNT)

def update_cache(CACHE_FILE, list_posted):

	with open(CACHE_FILE, mode="w") as file:
		file.write(json.dumps(list_posted))

def get_valid_ids(origin_chat):

	chat_ids=[]
	print('Getting messages...')
	his=useraccount.get_chat_history(origin_chat)
	for message in his:chat_ids.append(message.id)
	last_message_id=chat_ids[0]
	chat_ids.sort()

	return last_message_id,chat_ids

def get_files_type_excluded():

	global FILES_TYPE_EXCLUDED
	try:
		FILES_TYPE_EXCLUDED = FILES_TYPE_EXCLUDED
		return FILES_TYPE_EXCLUDED
	except:
		FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input()
		return FILES_TYPE_EXCLUDED

def unknown_message(message, message_id, last_message_id) -> bool:

	if message.empty or message.service or message.dice or message.location:
		print(f"{message_id}/{last_message_id} (type not recognized)")
		wait_a_moment(message_id, skip=True)
		return True
	else:
		return False

def must_be_ignored(func_sender, message_id, last_message_id) -> bool:

	if func_sender in FILES_TYPE_EXCLUDED:
		print(f"{message_id}/{last_message_id} (skip by type)")
		wait_a_moment(message_id, skip=True)
		return True
	else:
		return False

def ensure_folder_existence(folder_path):
	"""If the folder does not exist, it 
	s
	Args:
		folder_path (str): folder path
	"""
	if not os.path.exists(folder_path):
		os.mkdir(folder_path)

def get_task_file(ORIGIN_CHAT_TITLE, destino):

	ensure_folder_existence("posteds")
	ensure_folder_existence(os.path.join("posteds"))
	task_file_name = f"{ORIGIN_CHAT_TITLE}-{destino}.json"
	task_file_path = os.path.join("posteds", task_file_name)
	return task_file_path

def check_chat_id(chat_id):

	try:
		chat_obj = tg.get_chat(chat_id)
		chat_title = chat_obj.title
		return chat_title
	except ChannelInvalid:  # When you are not part of the channel
		print("\nNon-accessible chat")
		if MODE == "bot":
			print(
				"\nCheck that the bot is part of the chat as an administrator."
				+ "It is necessary for bot mode."
			)
		else:
			print("\nCheck that the user account is part of the chat.")
		return False
	except PeerIdInvalid:  # When the chat_id is invalid
		print(f"\nInvalid chat_id: {chat_id}")
		return False

def main():

	global FILES_TYPE_EXCLUDED
	FILES_TYPE_EXCLUDED = get_files_type_excluded()
	last_message_id,chat_ids=get_valid_ids(origin_chat)

	int_task_type = NEW
	list_posted = get_list_posted(int_task_type)

	ids_to_try=chat_ids[len(list_posted):]

	for message_id in ids_to_try:

		message = get_message(origin_chat, message_id)

		if unknown_message(message, message_id, last_message_id):
			list_posted += [message.id]
			continue

		func_sender = get_sender(message)

		if must_be_ignored(func_sender, message_id, last_message_id):
			list_posted += [message.id]
			update_cache(CACHE_FILE, list_posted)
			continue

		func_sender(message, destino)
		print(f"{message_id}/{last_message_id}")

		list_posted += [message.id]
		update_cache(CACHE_FILE, list_posted)

		wait_a_moment(message_id)

config_data = get_config_data(os.path.join("config.ini"))
USER_DELAY_SECONDS = float(config_data.get("user_delay_seconds"))
BOT_DELAY_SECONDS = float(config_data.get("bot_delay_seconds"))
SKIP_DELAY_SECONDS = float(config_data.get("skip_delay_seconds"))
BOT_ID=config_data.get("bot_id")

parser = argparse.ArgumentParser()
parser.add_argument("--orig")
parser.add_argument("--dest")
parser.add_argument("--mode",choices=["user", "bot"])
parser.add_argument("--new", type=int, choices=[1, 2])
parser.add_argument("--type")
options = parser.parse_args()

os.system("clear||cls")

MODE = options.mode

useraccount = ensure_connection("user")
if MODE == "bot":
	bot = ensure_connection("bot")
	tg = bot
	DELAY_AMOUNT = BOT_DELAY_SECONDS

if MODE == "user":
	tg = useraccount
	DELAY_AMOUNT = USER_DELAY_SECONDS

DELAY_SKIP = SKIP_DELAY_SECONDS
NEW = options.new

if __name__=="__main__":
	get_chats()
	start()