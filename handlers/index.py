from handler import *
from model import News

@handler('index', authed=False)
def get_index():
	if session.user == None:
		redirect(handler.auth.get_index)

	return dict(
		news=News.getLast(5)
	)

@handler('support', authed=True)
def get_support():
	pass

@handler('support_complete', authed=True)
def post_support_create(message):
	pass
