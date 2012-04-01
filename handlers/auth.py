from handler import handler
from model import User
from flask import session

@handler
def get_login(username=None, password=None):
	user = User.find(username, password)
	if user == None:
		return 'Login failed'

	session['userId'] = user.id
	return 'Success'

@handler
def get_register(username=None, password=None):
	if username == None or password == None:
		return ''

	if len(username) < 3 or len(password) < 8:
		return 'Username must be 3 or more characters.  Password must be 8 or more characters.'

	user = User.add(username, password, False)
	if user == None:
		return 'Username taken.'
	return 'Woot.'
