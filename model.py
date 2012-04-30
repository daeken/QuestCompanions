import math, json, os, random
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.types import *
from sms import sms

from metamodel import *
import hashlib
import markdown2

@Model
class Feedback(object):
	profile_id = ForeignKey(Integer, 'User.id')
	helpful = Boolean
	date = DateTime
	body = Unicode()

@Model
class FAQ(object):
	creator_id = ForeignKey(Integer, 'User.id')
	question = Unicode()
	answer = Unicode()
	answer_markdown = Unicode()

@Model
class News(object):
	creator_id = ForeignKey(Integer, 'User.id')
	headline = Unicode()
	story = Unicode()
	story_markdown = Unicode()

	@staticmethod
	def getLast(number=5):
		return transact.query(News).order_by(News.id.desc()).limit(number).all()

# Games
WOW = 1
SWTOR = 2

def gamename(id):
	if id == WOW:
		return 'WoW'
	elif id == SWTOR:
		return 'SW:TOR'

@Model
class GoldHistory(object):
	user_id = ForeignKey(Integer, 'User.id')
	date = DateTime
	amount = Integer
	balance = Integer
	dollars = Integer
	job_id = ForeignKey(Integer, 'Job.id', nullable=True)
	desc = Unicode

@Model
class Bid(object):
	job_id = ForeignKey(Integer, 'Job.id')
	char_id = ForeignKey(Integer, 'Character.id')
	amount = Integer
	date = DateTime
	accepted = Boolean

	def accept(self):
		with transact:
			self.update(accepted=True)
			self.job.update(accepted_date=datetime.now())

@Model
class Job(object):
	user_id = ForeignKey(Integer, 'User.id')
	char_id = ForeignKey(Integer, 'Character.id')
	game = Integer
	created_date = DateTime

	max_pay = Integer
	time_reqd = Integer
	desc = Unicode(140)
	reqs = String

	bids = Bid.relation(backref='job')

	canceled = Boolean
	accepted_date = Nullable(DateTime())
	timer_flags = Integer
	timer_started = Nullable(DateTime())
	completed = Boolean
	fee_paid = Integer

	gold_history = GoldHistory.relation(backref='job')

	@staticmethod
	def add(char, max_pay, time_reqd, desc, **kwargs):
		with transact:
			return Job.create(
				user=char.user, 
				char=char, 
				game=char.game, 
				created_data=datetime.now(), 
				max_pay=max_pay, 
				time_reqd=time_reqd,
				desc=desc, 
				reqs=json.dumps(kwargs), 
				timer_flags=0, 
				completed=False, 
				canceled=False, 
				fee_paid=0
			)

	def gamename(self):
		return gamename(self.game)

	def bid(self, char, amount):
		with transact:
			return Bid.create(
					job=self, 
					char=char, 
					amount=amount, 
					date=datetime.now()
				)

	def complete(self):
		accepted = None
		for bid in self.bids:
			if bid.accepted:
				accepted = bid
				break
		assert accepted
		accepted_user = accepted.char.user
		with transact:
			fee = int(math.ceil(float(accepted.amount) * 0.3))
			earned = accepted.amount-fee
			self.update(completed=True, fee_paid=fee)
			self.user.update(gold=self.user.gold-accepted.amount)
			GoldHistory.create(
					user=self.user, 
					date=datetime.now(), 
					amount=-accepted.amount, 
					balance=self.user.gold, 
					job=self, 
					desc=u'Paid %i gold for a job' % accepted.amount
				)
			accepted_user.update(gold=accepted_user.gold+earned)
			GoldHistory.create(
					user=accepted_user, 
					date=datetime.now(), 
					amount=earned, 
					balance=accepted_user.gold, 
					job=self,
					desc=u'Earned %i gold for a job' % (earned)
				)

@Model
class Character(object):
	user_id = ForeignKey(Integer, 'User.id')
	game = Integer

	name = Unicode()
	server = Nullable(Unicode())
	avatar = String()
	attrs = String()
	last_update = Date()

	jobs = Job.relation(backref='char')
	bids = Bid.relation(backref='char')

	def gamename(self):
		return gamename(self.game)

	def link(self, cls='charLink'):
		from handler import handler
		return '<a class="%s" data-char=%s href="%s">%s</a>' %\
			(cls, self.json(), handler.char.get_index.url(self.id), self.name.replace('<', '&lt;'))

	def imagelink(self, cls='charLink'):
		from handler import handler
		return '<img class="%s" data-char=%s src="%s" alt="%s">' %\
			(cls, self.json(), self.avatar.replace('"', '&quot;'), self.name.replace('"', '&quot;'))

	def json(self):
		val = dict(
				game=gamename(self.game), 
				name=self.name, 
				server=self.server, 
				avatar=self.avatar,
			)
		if self.attrs:
			val.update(json.loads(self.attrs))
		val = '"%s"' % json.dumps(val).replace('"', '&quot;')
		return val

	def eligible(self, job):
		char = job.char
		if char.id == self.id or self.game != char.game or self.server != char.server:
			return False
		return True

@Model
class User(object):
	enabled = Boolean
	admin = Boolean
	username = Unicode(255)
	password = String(88)
	gold = Integer
	email = String
	email_verified = Boolean
	email_verification = String
	email_notifications = Boolean
	phone_number = String
	phone_verified = Boolean
	phone_verification_code = Integer
	phone_verification_tries = Integer
	phone_notifications = Boolean
	feedback_score = Integer
	feedback_positive = Integer
	feedback_negative = Integer

	characters = Character.relation(backref='user')
	news = News.relation(backref='creator')
	jobs = Job.relation(backref='user')
	gold_history = GoldHistory.relation(backref='user')
	feedbacks = Feedback.relation(backref='profile')


	@staticmethod
	def hash(password):
		salt = ''.join('%02x' % ord(c) for c in os.urandom(24))
		for i in range(1000):
			password = hashlib.sha1(salt + password + salt).hexdigest()
		return salt+password

	@staticmethod
	def checkHash(hash, password):
		salt, hash = hash[:48], hash[48:]
		for i in range(1000):
			password = hashlib.sha1(salt + password + salt).hexdigest()
		if password == hash:
			return True
		return False

	@staticmethod
	def add(username, password, admin):
		if User.one(enabled=True, username=username):
			return None
		with transact:
			return User.create(
				enabled=True, 
				username=username, 
				password=User.hash(password), 
				admin=admin, 
				gold=0, 
				phone_number='', 
				phone_verified=False, 
				phone_notifications=True, 
				email='', 
				email_verified=False,
				email_notifications=True, 
				feedback_score = 0,
				feedback_positive = 0,
				feedback_negative = 0
			)
	
	@staticmethod
	def find(username, password):
		if username == None or password == None:
			return None
		user = User.one(enabled=True, username=username)
		if user and User.checkHash(user.password, password):
			return user
		return None
	
	def change(self, email=None):
		if email != None and email != self.email:
			with transact:
				self.update(
						email=email, 
						email_verified=False
					)
			self.generateEmailVerification()

	def generateEmailVerification(self):
		from handler import email
		code = ''.join('%02X' % random.randrange(256) for i in range(20))
		with transact:
			self.update(email_verification=code)
		email(self.email, 'verify', code=code)

	def addGold(self, amount, price):
		with transact:
			self.update(gold=self.gold+amount)
			GoldHistory.create(
					user=self, 
					date=datetime.now(), 
					amount=amount, 
					balance=self.gold, 
					dollars=price, 
					job=None, 
					desc=u'Bought %i gold for $%.2f' % (amount, price / 100.0)
				)

	def sms(self, message):
		if not self.phone_verified:
			return False

		sms(self.phone_number, message)
		return True

@Model
class Config(object):
	name = String(20)
	value = Unicode(255)

	@staticmethod
	def get(name):
		try:
			return Config.one(name=name).value
		except:
			return None

	@staticmethod
	def getString(name):
		data = Config.get(name)
		if data == None:
			return None
		else:
			return str(data)

	@staticmethod
	def set(name, value):
		with transact:
			try:
				row = Config.one(name=name)
				row.update(value=unicode(value))
			except:
				Config.create(
					name=name,
					value=unicode(value)
				)

try:
	file('prod', 'r')
	db = 'postgresql://postgres:postgresqc@localhost/qc'
except:
	db = 'sqlite:///model.db'
@setup(db)
def init():
	admin = User.add(u'admin', 'admin', True)
