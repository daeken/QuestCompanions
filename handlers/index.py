from handler import *
from model import News

@handler('index', authed=False)
def get_index():
	if session.user == None:
		redirect(handler.auth.get_index)

	return dict(
		news=News.getLast(5)
	)
