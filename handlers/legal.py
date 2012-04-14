from handler import *

@handler('legal/privacy', authed=False)
def get_privacy():
	pass

@handler('legal/tos', authed=False)
def get_tos():
	pass
