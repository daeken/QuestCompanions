from handler import handler
from flask import session

@handler
def get_index():
	if session.user:
		return 'Hi ' + session.user.username
	return 'Hi'
