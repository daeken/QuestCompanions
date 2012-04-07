from handler import *
from model import *

@handler('admin/index', admin=True)
def get_index():
	pass

@handler('admin/news', admin=True)
def get_news():
	return dict(news=News.all())

@handler('admin/news_story', admin=True)
def get_news(id):
	return dict(story=News.one(id=int(id)))

@handler('admin/news_story', admin=True)
def post_save_news(id, headline, story):
	sobj = News.one(id=int(id))
	with transact:
		sobj.update(headline=headline, story=story)
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
