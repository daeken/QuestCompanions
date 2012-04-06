from handler import *
from model import News, User

@handler('admin/index', admin=True)
def get_index():
	pass

@handler('admin/news', admin=True)
def get_news():
	return dict(news=News.all())

@handler('admin/news_story', admin=True)
def get_news(id):
	return id
