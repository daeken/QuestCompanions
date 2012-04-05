from handler import *

@handler('index')
def get_index():
	if session.user == None:
		redirect(handler.auth.get_index)

	return dict(
		user=session.user,
		news=[]
	)
