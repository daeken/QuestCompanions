from handler import handler

@handler
def get_index(id, bar=None):
	return 'foo %r %r' % (id, bar)
