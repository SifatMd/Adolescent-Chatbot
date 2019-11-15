import os, sys
from flask import Flask, request
from utils import wit_nlp
from pymessenger import Bot
import database
from emoji_handler import emoji_handler
from chatterbot_response import *


log_file = open("log.txt", "w")

app = Flask(__name__)

#PAGE_ACCESS_TOKEN = "EAAEygDY4BKEBAMvhzQg56TUuyZCIxzqOKz3rYZByYhkMi15mhYVzXQ8GtZBD3NGgNfDjTfGdH0oNLnvBtk1ZBH8svDIruuOPmZC5oDxKhBfuzArgQv9jo6zgOhxzHfTJQEMFMTToEw2Nfzd1lzzCqnh3AJuhchfUBwbryvrpxEwZDZD"
PAGE_ACCESS_TOKEN = "EAAKwt1crztYBAFwHx2rbboliy4Xb4otOE1UTaa9soFJ93ta0jYxxzrxBl6sWThsLZADBwe5DGb4wzhRdg8GmZA8ZA33sr3RXgNI05Dhq8t8SqBPRTDgIZBrpn5d9e0omhDDqz9uyBHL39ZC7DdFEfDH7oWO0VdAytZCeoRAEirJ4bndmLw0FfzJXUILVb6c7cZD"

bot = Bot(PAGE_ACCESS_TOKEN)

users = dict()


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world, Snigdho", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	# print(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if sender_id not in users:
					users[sender_id] = ["null", "null"]

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'


					if emoji_handler(bot, messaging_text, sender_id):
						return "ok", 200

					if get_chatterbot_response(bot, messaging_text, sender_id):
						return "ok", 200

					response = None

					subject, intent = wit_nlp(messaging_text)

					if intent == "greetings":
						response = "Hello! আপনাকে কীভাবে সহায়তা করতে পারি?"
						bot.send_text_message(sender_id, response)
						return "ok", 200
						

					if subject == "null" and intent == "null":

						users[sender_id][0] = "null"
						users[sender_id][1] = "null"

						#TODO: response = MATCH FROM GREETINGS TABLE AND GENERIC TABLE	 
						response = "দুঃখিত, আমি আপনার কথা বুঝতে পারছি না।"
						bot.send_text_message(sender_id, response)

						options = database.get_subjects()
						send_options(sender_id, "আমি আপাতত শুধু এই সমস্যাগুলোর বিষয়ে জানিঃ", options)
						return "ok", 200


					elif subject == "null":
						if users[sender_id][0] != "null":
							subject = users[sender_id][0]
							response = database.get_response({'text':messaging_text, 'intent':intent, 'subject':subject})
							users[sender_id][0] = "null"
							users[sender_id][1] = "null"
							bot.send_text_message(sender_id, response)
							return "ok", 200
						else:
							users[sender_id][0] = "null"
							users[sender_id][1] = "null"
							response = "আপনি কী বিষয়ে জানতে চান?"
							bot.send_text_message(sender_id, response)

							return "ok", 200


					elif intent == "null": # subject detected
						if database.record_exists(subject):

							users[sender_id][0] = subject
							users[sender_id][1] = "null"

							response = "আপনি " + subject + " এর ব্যাপারে কী সহায়তা চান?"
							bot.send_text_message(sender_id, response)
							return "ok", 200

						else:
							response = "দুঃখিত, " + subject + " এর ব্যাপারে আমার কাছে কোনো তথ্য নেই।"
							bot.send_text_message(sender_id, response)

							options = database.get_subjects()
							send_options(sender_id, "আমি আপাতত শুধু এই সমস্যাগুলোর বিষয়ে জানিঃ", options)

							users[sender_id][0] = "null"
							users[sender_id][1] = "null"
							return "ok", 200

					else:
						response = database.get_response({'text':messaging_text, 'intent':intent, 'subject':subject})
						bot.send_text_message(sender_id, response)
						users[sender_id][0] = "null"
						users[sender_id][1] = "null"
						return "ok", 200
					# log_file.write(sender_id + os.linesep)

	return "ok", 200


def send_options(recipient_id, text, options):

	quick_replies = []
	for option in options:
		quick_replies.append({"content_type":"text", "title":option, "payload":option})

	bot.send_message(recipient_id, {"text": text, "quick_replies": quick_replies})


if __name__ == "__main__":
	app.run(debug = True, port = 80)
