from flask import request, session
from model import User

all = {}

def handler(func):
	name = func.func_name
	if name.startswith('get_'):
		name = name[4:]
		method = 'GET'
	elif name.startswith('post_'):
		name = name[5:]
		method = 'POST'
	else:
		raise Exception('All handlers must be marked get_ or post_.')

	module = func.__module__.split('.')[-1]
	if not module in all:
		all[module] = {}
	args = func.__code__.co_varnames[:func.__code__.co_argcount]

	ofunc = func
	def func(id=None):
		try:
			if 'userId' in session:
				session.user = User.one(id=int(session['userId']))
			else:
				session.user = None
			params = request.form if method == 'POST' else request.args
			kwargs = {}
			for i, arg in enumerate(args):
				if i == 0 and arg == 'id':
					continue
				if arg in params:
					kwargs[arg] = params[arg]

			if id != None:
				return ofunc(id, **kwargs)
			else:
				return ofunc(**kwargs)
		except:
			import traceback
			traceback.print_exc()

	func.func_name = '__%s__%s__' % (module, name)
	all[module][name] = method, args, func
	return func
