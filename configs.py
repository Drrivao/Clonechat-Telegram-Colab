from pyrogram import Client
import argparse
from os import remove,system

parser = argparse.ArgumentParser()
parser.add_argument('-i','--api_id')
parser.add_argument('-s','--api_hash')
parser.add_argument('-b','--bot_token')
options = parser.parse_args()

def main(API_ID,API_HASH,BOT_TOKEN):

	system("clear||cls")
	
	if BOT_TOKEN is None:
		BOT_TOKEN='blank'

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
		remove('user.session')
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
			remove('bot.session')
			print(f"Connection failed due to {e}.")
	else: BOT_ID=''

	data=f"[default]\n{BOT_ID}\nuser_delay_seconds:10\n"+\
	"bot_delay_seconds:1.2\nskip_delay_seconds:1"
	
	with open('config.ini', 'w') as f:
		f.write(data)

if __name__=="__main__":

	main(
		options.api_id,
		options.api_hash,
		options.bot_token
	)