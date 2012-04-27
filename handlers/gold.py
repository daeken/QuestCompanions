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
				description=u'%s bought %i gold on QuestCompanions' % (session.user.username, gold)
			)
	except e:
		return e.message, -1
	
	session.user.addGold(gold, gold_map[gold] * 100)

	return None, session.user.gold

@handler('gold/history')
def get_history():
	history = session.user.gold_history
	history.reverse()
	return dict(history=history)

@handler('gold/withdraw')
def get_withdraw():
	outstanding = 0
	for job in session.user.jobs:
		if not job.completed and not job.canceled:
			outstanding += job.max_pay
	return dict(gold=session.user.gold - outstanding)

@handler('gold/withdraw_completed')
def post_withdraw(amount, name, address):
	amount = int(amount)
	outstanding = 0
	for job in session.user.jobs:
		if not job.completed and not job.canceled:
			outstanding += job.max_pay
	if amount < 0 or amount > session.user.gold - outstanding:
		redirect(get_withdraw)

	price = amount * 10 # Put it into cents
	user = session.user
	with transact:
		user.update(gold=user.gold - amount)
		GoldHistory.create(
				user=user, 
				date=datetime.now(), 
				amount=-amount, 
				balance=user.gold, 
				dollars=price, 
				job=None, 
				desc=u'Withdrew %i gold for $%.2f' % (amount, price / 100.0)
			)
	email('cody@questcompanions.com', 'withdrawal', user=user, gold=amount, usd=price/100.0, address=u'%s\n%s' % (name, address))
	redirect(get_withdraw)
