from handler import *
from model import *
import markdown2

@handler('admin/index', admin=True)
def get_index():
	pass

@handler('admin/news', admin=True)
def get_news():
	return dict(news=News.all())

@handler('admin/news_story', admin=True)
def get_news(id):
	return dict(story=News.one(id=id))

@handler('admin/news_create', admin=True)
def get_news_create():
	pass

@handler('admin/news_create', admin=True)
def post_news_create(headline, story):
	with transact:
		News.create(
				headline=headline, 
				story=story,
				story_markdown=markdown2.markdown(story)
			)
	redirect(get_news)

@handler('admin/news_story', admin=True)
def post_save_news(id, headline, story):
	sobj = News.one(id=id)
	with transact:
		sobj.update(headline=headline, story=story,
				story_markdown=markdown2.markdown(story))
	redirect(get_news)

@handler('admin/users', admin=True)
def get_user():
	return dict(users=User.all())

@handler('admin/user_create', admin=True)
def get_user_create():
	pass

@handler(admin=True)
def post_user_create(username, password, admin=False):
	user = User.add(username, password, admin == u'on')
	if user == None:
		redirect(get_user_create)
	redirect(get_user)

@handler('admin/faq', admin=True)
def get_faq():
	return dict(faqs=FAQ.all())

@handler('admin/faq_edit', admin=True)
def get_faq(id):
	return dict(faq=FAQ.one(id=id))

@handler('admin/faq_edit', admin=True)
def get_faq_create():
	return dict(faq=None)

#Edit and create
@handler(admin=True)
def post_faq_edit(_id, question, answer):
	with transact:
		if _id == u'':
			FAQ.create(
					question=question, 
					answer=answer,
					answer_markdown=markdown2.markdown(answer)
				)
		else:
			faq = FAQ.one(id=int(_id))
			faq.update(
					question=question, 
					answer=answer,
					answer_markdown=markdown2.markdown(answer)
				)
	redirect(get_faq)

def goldusd(gold):
	return gold * 10.0

@handler('admin/stats', admin=True)
def get_stats():
	user_count = len(User.all())
	jobs_completed = len(Job.some(completed=True))
	jobs_total = len(Job.all())
	fees = sum(job.fee_paid for job in Job.some(completed=True))

	history = GoldHistory.all()
	deposits = 0
	deposit_gold = 0
	deposit_dollars = 0
	withdrawals = 0
	withdrawal_gold = 0
	withdrawal_dollars = 0
	for elem in history:
		if elem.job != None:
			continue
		if elem.amount < 0:
			withdrawals += 1
			withdrawal_gold -= elem.amount
			withdrawal_dollars += elem.dollars
		else:
			deposits += 1
			deposit_gold += elem.amount
			deposit_dollars += elem.dollars

	total_gold = sum(user.gold for user in User.all())

	return dict(
			user_count=user_count, 
			jobs_completed=jobs_completed, 
			jobs_total=jobs_total, 
			fees=fees, 
			fees_usd=goldusd(fees), 
			deposits=deposits, 
			withdrawals=withdrawals, 
			deposit_gold=deposit_gold, 
			withdrawal_gold=withdrawal_gold, 
			deposit_dollars=deposit_dollars, 
			withdrawal_dollars=withdrawal_dollars, 
			total_gold=total_gold, 
			total_dollars=goldusd(total_gold), 
		)
