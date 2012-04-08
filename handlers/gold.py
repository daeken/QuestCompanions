import stripe
from handler import *
from model import *

stripe.api_key = 'akA7Aw3aFIcAb8UstFLBWcMFO6QIFcKY'

@handler('gold/index')
def get_index():
	pass

@handler('gold/buy')
def get_buy():
	pass

gold_map = {
	50: 5, 
	105: 10, 
	220: 20, 
	575: 50
}

@handler
def rpc_buy(token, gold):
	gold = int(gold)
	if gold not in gold_map:
		return 'Invalid gold amount'
	try:
		charge = stripe.Charge.create(
				amount=gold_map[gold]*100, 
				currency='usd', 
				card=token, 
				description='Bought %i gold on QuestCompanions' % gold
			)
	except e:
		return e.message, -1
	
	with transact:
		session.user.update(gold=session.user.gold+gold)

	return None, session.user.gold
