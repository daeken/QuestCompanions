from twilio.rest import TwilioRestClient

account = 'AC8a71a65b3b8cdf7110b2d978b36a44bd'
token = '82efda0de44c9c2cf63cb8e4722655fe'
from_number = '+18456783780'

def sms(number, message):
	client = TwilioRestClient(account, token)
	if number[0] != '+':
		if number[0] == '1':
			number = '+' + number
		else:
			assert len(number) == 10
			number = '+1' + number
	client.sms.messages.create(to=number, from_=from_number, body=message)
