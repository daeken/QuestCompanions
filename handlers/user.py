from handler import handler
from model import User

@handler('user.tpl')
def get_index(id):
	user = User.one(id=int(id))

	return dict(user=user)
