from handler import *
from model import News

@handler('news_story', authed=True)
def get_index(id):
	return dict(
		story=News.one(id=id)
	)
