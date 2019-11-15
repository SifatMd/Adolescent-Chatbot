from wit import Wit
import sys

#wit_access_token = "XAU4I3Y35BTJTCSR2JOI2OSRV5EGVQT7" #doesnt match according to Server Access token
wit_access_token = "3S6NUOOCITD35MQ5D5GZBOPQ7VKYWYDU"
client = Wit(access_token = wit_access_token)

def wit_nlp(message_text):
	resp = client.message(message_text)
	
	subject = "null"
	intent 	= "null"

	try:
		subject = resp['entities']['subject'][0]['value']
	except:
		pass
	try:
		intent = resp['entities']['intent'][0]['value']
	except:
		pass

	print(message_text, subject, intent)
	sys.stdout.flush()

	return (subject, intent)




wit_nlp("ব্রনে অনেক চুলকাচ্ছে।")

