import hmac
from datetime import datetime
from time import mktime
from handler import *
from model import *

def genInvite():
	code = '%i.%i' % (session.user.id, mktime(datetime.now().timetuple()))
	return code + hmac.new(Config.getString('secret_key'), code).hexdigest()[:8]

@handler('invite/index')
def get_index():
	return dict(invite_url='https://questcompanions.com' + get_accept.url(code=genInvite()))

@handler('invite/index')
def post_index(email):
	if u'@' not in email or '\n' in email or '\r' in email or ',' in email:
		return dict(error='Invalid email')
	elif len(User.some(email=email)):
		return dict(alert='Your friend is already a QuestCompanions member')

	code = genInvite()

	handler.email(email, 'invite', code=code, username=None if session.user.admin else session.user.username)

	return dict(alert='Invite sent successfully!')

def codeCheck(code):
	code, mac = code[:-8], code[-8:]
	return hmac.new(Config.getString('secret_key'), code).hexdigest()[:8] == mac

@handler('invite/accept', authed=False)
def get_accept(code=None):
	if session.user != None:
		redirect(handler.index.get_index.url(error='You\'re already registered'))
	elif code == None or not codeCheck(code):
		return dict(error='Invalid invitation code')
	return dict(code=code)

@handler('invite/accept', authed=False)
def post_accept(code, username, password, email):
	if session.user != None:
		redirect(handler.index.get_index.url(error='You\'re already registered'))
	elif code == None or not codeCheck(code):
		return dict(error='Invalid invitation code')

	error = None
	if User.one(username=username):
		error = u'Username is taken'
	elif len(password) < 6:
		error = u'Password must be at least 6 characters'
	elif u'@' not in email or '\n' in email or '\r' in email or ',' in email:
		error = u'Invalid email'

	if error:
		return dict(code=code, username=username, email=email, error=error)

	user = User.add(username, password, False)
	user.change(email=email)

	session['userId'] = user.id

	redirect(handler.index.get_index.url(alert='Congratulations!  You\'re all set up.  Check your email for the verification.'))
