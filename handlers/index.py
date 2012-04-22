from handler import *
from model import *

@handler('index', authed=False)
def get_index():
	if session.user == None:
		redirect(handler.auth.get_index)
  
	alljobs = Job.some(completed=False)
	jobs = []
	for job in alljobs:
		if job.canceled:
			continue
		if job.accepted_date == None or job.user == session.user or \
			len([bid for bid in job.bids if bid.accepted and bid.char.user == session.user]) == 1:
			jobs.append(job)
	return dict(
		news=News.getLast(5), jobs=jobs
	)

@handler('support', authed=True)
def get_support():
	pass

@handler('support_complete', authed=True)
def post_support_create(message):
	pass

@handler('faq', authed=False)
def get_faq():
	faqs = FAQ.all()
	return dict(faqs=faqs)
