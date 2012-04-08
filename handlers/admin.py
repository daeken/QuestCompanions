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
	return dict(story=News.one(id=int(id)))

@handler('admin/news_create', admin=True)
def get_news_create():
	pass

@handler('admin/news_create', admin=True)
def post_create_news(headline, story):
	with transact:
		News.create(
				headline=headline, 
				story=story,
				story_markdown=markdown2.markdown(story)
			)
	redirect(get_news)

@handler('admin/news_story', admin=True)
def post_save_news(id, headline, story):
	sobj = News.one(id=int(id))
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
def post_create_user(username, password, admin=False):
	user = User.add(username, password, admin == u'on')
	if user == None:
		redirect(get_user_create)
	redirect(get_user)

@handler('admin/faq', admin=True)
def get_faq():
	return dict(faqs=FAQ.all())

@handler('admin/faq_edit', admin=True)
def get_faq(id):
	return dict(faq=FAQ.one(id=int(id)))

@handler('admin/faq_edit', admin=True)
def get_faq_create():
	return dict(faq=None)

@handler(admin=True)
def post_edit_faq(_id, question, answer):
	with transact:
		if _id == u'':
			FAQ.create(
					question=question, 
					answer=answer
				)
		else:
			faq = FAQ.one(id=int(_id))
			faq.update(
					question=question, 
					answer=answer
				)
	redirect(get_faq)
