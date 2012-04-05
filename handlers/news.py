from handler import *
from model import News

@handler('news_story')
def get_index(id):
	return dict(
		story=News.one(id=int(id))
	)
