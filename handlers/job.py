from handler import *
from model import *

@handler('jobs/index', authed=True)
def get_index():
	jobs = Job.some(accepted_date=None)
	return dict(jobs=jobs)

@handler('jobs/job', authed=True)
def get_index(id):
	job = Job.one(id=int(id))
	return dict(job=job)

@handler('jobs/create', authed=True)
def get_create():
	return dict(chars=session.user.characters)

@handler(authed=True)
def post_job_create(char, desc, time_reqd, max_pay):
	char = Character.one(id=char)
	time_reqd = int(time_reqd)
	max_pay = int(max_pay)
	if char == None or char.user != session.user or len(desc) > 140 or time_reqd < 1 or max_pay < 10:
		abort(403)

	job = Job.add(char, max_pay, time_reqd, desc)
	redirect(get_index.url(job.id))
