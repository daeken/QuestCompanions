from handler import *
from model import *
from wow_servers import wow_servers
import battlenet

@handler('char/profile')
def get_index(id):
	char = Character.one(id=int(id))
	if not char: abort(404)

	return dict(char=char)

@handler('char/create')
def get_create():
	return dict(
			wow_servers=wow_servers
		)

@handler
def rpc_add_wow(server, charname):
	try:
		wowchar = battlenet.Character(battlenet.UNITED_STATES, server, charname)
	except:
		return False

	thumbnail = 'https://us.battle.net/static-render/us/' + wowchar.thumbnail
	with transact:
		char = Character.create(
				user=session.user,  
				game=WOW, 
				name=wowchar.name, 
				server=server, 
				avatar=thumbnail, 
				attrs=''
			)

	return get_index.url(char.id)
