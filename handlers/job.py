from handler import *
from model import *
import thread, time

@handler('jobs/index')
def get_index():
	alljobs = Job.some(completed=False)
	jobs = []
	for job in alljobs:
		if job.canceled:
			continue
		if (job.user == session.user or 
			len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 1):
			jobs.append(job)
		if job.accepted_date == None:
			for char in session.user.characters:
				if char.eligible(job):
					jobs.append(job)
					break
	
	return dict(jobs=jobs)

@handler('jobs/job')
def get_index(id):
	job = Job.one(id=id)
	bids = accepted = None
	if job.accepted_date != None:
		accepted = [bid for bid in job.bids if bid.accepted][0]
	elif not job.canceled:
		bids = []
		users = []
		all = job.bids
		all.reverse()
		for bid in all:
			if bid.char.user.id in users:
				continue
			users.append(bid.char.user.id)
			bids.append(bid)
		bids.sort(lambda a, b: cmp(a.amount, b.amount))
	return dict(
		job=job, 
		accepted=accepted, 
		bids=bids, 
		min_bid=bids[0].amount if bids and len(bids) else job.max_pay, 
		canceled=job.canceled
	)

@handler('jobs/create')
def get_create():
	outstanding = 0
	for job in session.user.jobs:
		if not job.completed and not job.canceled:
			outstanding += job.max_pay
	return dict(
			chars=session.user.characters, 
			gold=session.user.gold-outstanding, 
			outstanding=outstanding
		)

def dispatch_notifications(id):
	job = Job.one(id=id)
	userchars = {}
	for char in Character.some(game=job.char.game, server=job.char.server):
		if char.eligible(job):
			if char.user.id not in userchars:
				userchars[char.user.id] = []
			userchars[char.user.id].append(char)

	for id, chars in userchars.items():
		if len(chars) == 1:
			charstr = 'character %s' % chars[0].name
		else:
			first, end = ', '.join(char.name for char in chars[:-1]), chars[-1].name
			if len(chars) > 2:
				first += ', '
			charstr = 'characters %s and %s' % (first, end)
		if char.user.phone_notifications:
			char.user.sms(
				'Greetings from QuestCompanions! Your %s %s eligible for a new job.  Bidding starts at %i gold.' % 
				(charstr, ('is' if len(chars) == 1 else 'are'), job.max_pay)
			)
		if char.user.email and char.user.email_notifications:
			email(char.user.email, 'new_job', charstr=chartr, job=job, plural=len(chars) > 1, server=chars[0].server)

@handler
def post_job_create(char, desc, time_reqd, max_pay):
	char = Character.one(id=char)
	time_reqd = int(time_reqd)
	max_pay = int(max_pay)
	outstanding = 0
	for job in session.user.jobs:
		if not job.completed and not job.canceled:
			outstanding += job.max_pay
	if char == None or char.user != session.user or len(desc) > 140 or time_reqd < 1 or max_pay < 10 or max_pay > session.user.gold - outstanding:
		abort(403)

	job = Job.add(char, max_pay, time_reqd, desc)

	thread.start_new_thread(dispatch_notifications, (job.id, ))

	redirect(get_index.url(job.id))

@handler
def post_bid(id, amount, char):
	job = Job.one(id=id)
	char = Character.one(id=char)
	amount = int(amount)
	if (job == None or char == None or char.user != session.user or amount < 5 or 
		session.user == job.user or amount > job.max_pay or job.canceled or job.accepted_date != None):
		redirect(get_index.url(id))

	job.bid(char, amount)

	redirect(get_index.url(id))

@handler
def rpc_accept_bid(id):
	bid = Bid.one(id=int(id))

	if bid.job.user != session.user or bid.job.accepted_date != None or bid.job.canceled:
		abort(403)

	bid.accept()
	return True

@handler('jobs/timer')
def get_timer(id):
	job = Job.one(id=id)
	accepted = Bid.one(job=job, accepted=True)
	if job.user != session.user and accepted.char.user != session.user:
		abort(403)
	elif job.completed:
		redirect(get_index.url(id))

	return dict(job=job, is_poster=job.user == session.user, payment=accepted.amount)

def epoch(dt):
	return time.mktime(dt.utctimetuple()) + dt.microsecond/1000000.

def time_offset(dt):
	now = epoch(datetime.utcnow())
	return epoch(dt) - now

@handler
def rpc_check_active(id):
	job = Job.one(id=int(id))
	
	creator = job.user == session.user
	if (creator and job.timer_flags == 1) or (not creator and job.timer_flags == 2):
		return (1, 0)
	elif job.timer_flags == 3:
		return (2, time_offset(job.timer_started))
	else:
		return (0, 0)

@handler
def rpc_set_active(id):
	job = Job.one(id=int(id))
	
	creator = job.user == session.user
	with transact:
		flags = job.timer_flags | (1 if creator else 2)
		job.update(
			timer_flags=flags, 
			timer_started=datetime.utcnow() if flags == 3 else None
		)

	return (2 if flags == 3 else 1, time_offset(job.timer_started) if flags == 3 else 0)

@handler
def rpc_complete(id):
	job = Job.one(id=int(id))
	if job.user != session.user and \
		len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 0:
		abort(403)
	if job.completed:
		return
	job.complete()

@handler
def rpc_check_complete(id):
	job = Job.one(id=int(id))
	return job.completed

@handler
def rpc_cancel(id):
	job = Job.one(id=int(id))
	if job.user != session.user or job.completed or job.accepted_date != None:
		return

	with transact:
		job.update(canceled=True)

@handler
def post_feedback(id, helpful=None, body=u''):
	job = Job.one(id=id)
	if job == None or not job.completed:
		abort(403)
	if job.user == session.user:
		user = Bid.one(job=job, accepted=True).char.user
	elif len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 1:
		user = job.user
	else:
		abort(403)
	with transact:
		Feedback.create(
				profile_id=user.id,
				helpful= helpful==u'on',
				date=datetime.now(),
				body=body,
				)
		if helpful==u'on':
			user.update(
					feedback_positive=user.feedback_positive+1,
					feedback_score = int((float(user.feedback_positive+1) / (user.feedback_positive + user.feedback_negative + 1)) * 100)
					)
		else:
			user.update(
					feedback_negative=user.feedback_negative+1,
					feedback_score = int((float(user.feedback_positive) / (user.feedback_positive+user.feedback_negative+1)) * 100)
					)

	redirect(get_index.url(id))
