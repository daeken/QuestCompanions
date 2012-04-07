from handler import *
from model import User

@handler('user', authed=True)
def get_index(id):
	user = User.one(id=int(id))
	if not user: abort(404)

	return dict(user=user)
