from json import dumps
from flask import render_template, request, session
from model import User
from urllib import quote, urlencode

all = {}

def handler(tpl=None, json=False):
	def sub(func):
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
		hasId = len(args) > 0 and args[0] == 'id'

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
					ret = ofunc(id, **kwargs)
				else:
					ret = ofunc(**kwargs)
				if json:
					return dumps(ret)
				elif tpl != None:
					return render_template(tpl, **ret)
				else:
					return ret
			except:
				import traceback
				traceback.print_exc()

		func.func_name = '__%s__%s__' % (module, name)
		all[module][name] = method, args, func

		def url(_id=None, **kwargs):
			if module == 'index':
				url = '/'
			else:
				url = '/%s/' % module
			if name != 'index':
				url += '%s/' % name
			if hasId:
				assert _id != None
				url += quote(_id)
			if len(kwargs):
				url += '?'
				url += urlencode(kwargs)
			return url
		ofunc.url = url

		return ofunc

	if tpl != None and hasattr(tpl, '__call__'):
		func = tpl
		tpl = None
		return sub(func)
	return sub
