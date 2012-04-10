from handler import *
from model import *

@handler('jobs/index', authed=True)
def get_index():
	alljobs = Job.some(completed=False)
	jobs = []
	for job in alljobs:
		if job.accepted_date == None or job.user == session.user or \
			len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 1:
			jobs.append(job)
	return dict(jobs=jobs)

@handler('jobs/job', authed=True)
def get_index(id):
	job = Job.one(id=id)
	bids = accepted = None
	if job.accepted_date != None:
		accepted = [bid for bid in job.bids if bid.accepted][0]
	else:
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
		min_bid=bids[0].amount if bids and len(bids) else job.max_pay
	)

@handler('jobs/create', authed=True)
def get_create():
	return dict(chars=session.user.characters)

@handler
def post_job_create(char, desc, time_reqd, max_pay):
	char = Character.one(id=char)
	time_reqd = int(time_reqd)
	max_pay = int(max_pay)
	if char == None or char.user != session.user or len(desc) > 140 or time_reqd < 1 or max_pay < 10:
		abort(403)

	job = Job.add(char, max_pay, time_reqd, desc)
	redirect(get_index.url(job.id))

@handler
def post_bid(id, amount, char):
	job = Job.one(id=id)
	char = Character.one(id=char)
	amount = int(amount)
	if (job == None or char == None or char.user != session.user or amount < 5 or 
		session.user == job.user or amount > job.max_pay):
		redirect(get_index.url(id))

	if job.accepted_date == None:
		job.bid(char, amount)

	redirect(get_index.url(id))

@handler
def rpc_accept_bid(id):
	bid = Bid.one(id=int(id))

	if bid.job.user != session.user or bid.job.accepted_date != None:
		abort(403)

	bid.accept()
	return True

@handler('jobs/timer')
def get_timer(id):
	job = Job.one(id=id)
	#with transact:
	#	job.update(timer_flags=0)
	if job.user != session.user and \
		len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 0:
		abort(403)

	return dict(job=job)

@handler
def rpc_check_active(id):
	job = Job.one(id=int(id))
	
	creator = job.user == session.user
	if (creator and job.timer_flags == 1) or (not creator and job.timer_flags == 2):
		return 1
	elif job.timer_flags == 3:
		return 2
	else:
		return 0

@handler
def rpc_set_active(id):
	job = Job.one(id=int(id))
	
	creator = job.user == session.user
	with transact:
		flags = job.timer_flags | (1 if creator else 2)
		job.update(
			timer_flags=flags, 
			timer_started=datetime.now() if flags == 3 else None
		)

	return job.timer_flags
