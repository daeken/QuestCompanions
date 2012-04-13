import random, re
from sms import sms
from handler import *
from model import *

@handler('user/index')
def get_index(id):
	user = User.one(id=id)
	if not user: abort(404)

	return dict(user=user)

@handler
def post_index(id, phone_number=None):
	def normalize(phone_number):
		if phone_number == None:
			return user.phone_number
		return re.sub(r'[^0-9]', '', phone_number)

	user = User.one(id=id)
	if not user or user != session.user: abort(403)

	phone_number = normalize(phone_number)
	if phone_number != user.phone_number:
		with transact:
			user.update(
					phone_number=phone_number, 
					phone_verified=False
				)

	redirect(get_index.url(id))

@handler('user/verify')
def get_verify():
	if not session.user.phone_verified:
		with transact:
			session.user.update(
					verification_code=random.randrange(1000000), 
					verification_tries=0
				)
		sms(session.user.phone_number, 'Quest Companions verification code: %06i' % session.user.verification_code)

@handler('user/verify')
def post_verify(code):
	if session.user.verification_code == int(code):
		with transact:
			session.user.update(phone_verified=True)
		redirect(get_index.url(session.user.id))
	return dict(success=False, code=code)
