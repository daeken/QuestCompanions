from handler import *
from model import *
from wow_servers import wow_servers
import battlenet
from datetime import date

@handler('char/profile', authed=True)
def get_index(id):
	char = Character.one(id=id)
	if not char: abort(404)

	return dict(char=char)

@handler('char/create', authed=True)
def get_create(return_to=None):
	if return_to != None and return_to[0] != '/':
		abort(403)
	return dict(
			wow_servers=wow_servers, 
			return_to=return_to
		)

@handler(authed=True)
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
				name=wowchar.name.decode('utf-8'), 
				server=server, 
				avatar=thumbnail, 
				attrs='',
				last_update=date.today(),
				faction=wowchar.faction,
				level=wowchar.level,
				charclass=wowchar.get_class_name(),
				race=wowchar.get_race_name(),
				item_level=wowchar.equipment.average_item_level
			)

	return get_index.url(char.id)
