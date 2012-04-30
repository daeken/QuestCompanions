from handler import *
from model import *
import battlenet
from datetime import date
import urllib2
import json

@handler('login', authed=False)
def get_index():
	pass

@handler('login', authed=False)
def post_login(username=None, password=None):
	user = User.find(username, password)
	if user == None:
		return dict(username=username, error='Login failed')
	
	session['userId'] = user.id
	
	#Check for Character updates
	CurrentDate = date.today()
	for UserCharacter in user.characters:
		if UserCharacter.last_update < CurrentDate:
			if UserCharacter.game==WOW:
				try:
					wowchar = battlenet.Character(battlenet.UNITED_STATES,
							UserCharacter.server,
							UserCharacter.name)
				except:
					continue
				
				thumbnail = 'https://us.battle.net/static-render/us/' + wowchar.thumbnail
				with transact:
					if UserCharacter.attrs in ('', None):
						attrs = {}
					else:
						attrs = json.loads(UserCharacter.attrs)
					attrs = attrs.update(dict(
							faction = wowchar.faction,
							level = wowchar.level,
							charclass = wowchar.get_class_name(),
							race = wowchar.get_race_name(),
							item_level = wowchar.equipment.average_item_level
						))
					UserCharacter.update(
							avatar = thumbnail,
							last_update = CurrentDate,
							attrs = json.dumps(attrs)
					)
					#Add any other attributes that need to be updated.
				
			#if Character.game==SWTOR:
				#TODO Add SWTOR character info

	redirect(handler.index.get_index)

#@handler('register', authed=False)
def get_register():
	pass

#@handler(authed=False)
def post_register(username=None, password=None):
	if username == None or password == None:
		return ''

	if len(username) < 3 or len(password) < 8:
		return 'Username must be 3 or more characters.  Password must be 8 or more characters.'

	user = User.add(username, password, False)
	if user == None:
		return 'Username taken.'
	return 'Woot.'

@handler(authed=False)
def get_logout():
	session['userId'] = None

	redirect(handler.index.get_index)

@handler(authed=False)
def rpc_enlist(email): 
	APIKey = '2ffe157a9871aa5ed3a5e4c1eb4b2c91-us4'
	Server = 'us4'
	Payload = json.dumps({
		'email_address':email,
		'apikey':APIKey,
		'id':'f0fa9e4aae',
		'double_option':False,
		'send_welcome':True,
		'email_type':'html',
		'merge_vars':{'NAME':'Companion'}
		})

	URL = 'http://' + Server + '.api.mailchimp.com/1.3/?method=listSubscribe'
	Headers={'Content-Type':'application/json'}
	Request = urllib2.Request(URL, data=Payload, headers=Headers)
	Result = urllib2.urlopen(Request)
	JSONResponse = json.loads(Result.read())
	if JSONResponse is True:
		return True
	return False


