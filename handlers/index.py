from handler import *

@handler('index', authed=False)
def get_index():
	if session.user == None:
		redirect(handler.auth.get_index)

	return dict(
		user=session.user,
		news=[]
	)
