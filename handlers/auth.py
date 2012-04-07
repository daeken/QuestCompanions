from handler import *
from model import *
import battlenet
from datetime import date

@handler('login', authed=False)
def get_index():
	pass

@handler(authed=False)
def post_login(username=None, password=None):
	user = User.find(username, password)
	if user == None:
		return 'Login failed'
	
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
					UserCharacter.update(
							avatar = thumbnail,
							last_update = CurrentDate
					)
					#Add any other attributes that need to be updated.
				
			#if Character.game==SWTOR:
				#TODO Add SWTOR character info

	redirect(handler.index.get_index)

@handler('register', authed=False)
def get_register():
	pass

@handler(authed=False)
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
