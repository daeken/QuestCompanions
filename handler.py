from json import dumps
from flask import abort, render_template, request, session
from flask import redirect as _redirect
from werkzeug.exceptions import HTTPException
from model import User
from urllib import quote, urlencode

class ListObject(list):
	pass

class StrObject(str):
	pass

all = {}

def handler(_tpl=None, _json=False, admin=False, authed=True):
	def sub(func):
		name = func.func_name
		rpc = False
		tpl = _tpl
		json = _json
		if name.startswith('get_'):
			name = name[4:]
			method = 'GET'
		elif name.startswith('post_'):
			name = name[5:]
			method = 'POST'
		elif name.startswith('rpc_'):
			name = name[4:]
			method = 'POST'
			rpc = json = True
			tpl = None
		else:
			raise Exception('All handlers must be marked get_ or post_.')

		module = func.__module__.split('.')[-1]
		if not module in all:
			all[module] = ListObject()
			setattr(handler, module, all[module])
		args = func.__code__.co_varnames[:func.__code__.co_argcount]
		hasId = len(args) > 0 and args[0] == 'id' and not rpc

		ofunc = func
		def func(id=None):
			try:
				if 'userId' in session and session['userId']:
					session.user = User.one(id=int(session['userId']))
				else:
					session.user = None
				if (authed or admin) and session.user == None:
					abort(403)
				elif admin and not session.user.admin:
					abort(403)
				params = request.form if method == 'POST' else request.args
				kwargs = {}
				for i, arg in enumerate(args):
					if i == 0 and arg == 'id' and not rpc:
						continue
					if arg in params:
						kwargs[arg] = params[arg]
					else:
						assert not rpc # RPC requires all arguments.

				try:
					if hasId and id != None:
						ret = ofunc(id, **kwargs)
					else:
						ret = ofunc(**kwargs)
				except RedirectException, r:
					return _redirect(r.url)
				if json:
					return dumps(ret)
				elif tpl != None:
					if ret == None:
						ret = {}
					ret['handler'] = handler
					return render_template(tpl + '.html', **ret)
				else:
					return ret
			except HTTPException:
				raise
			except:
				import traceback
				traceback.print_exc()

		func.func_name = '__%s__%s__' % (module, name)

		def url(_id=None, **kwargs):
			if module == 'index':
				url = '/'
			else:
				url = '/%s/' % module
			if name != 'index':
				url += '%s/' % name
			if _id != None:
				url += quote(str(_id))
			if len(kwargs):
				url += '?'
				url += urlencode(dict((k, str(v)) for k, v in kwargs.items()))
			return url

		ustr = StrObject(url())
		ustr.__call__ = ofunc
		ustr.url = url
		func.url = url
		all[module].append((name, method, args, func, rpc))
		setattr(all[module], ofunc.func_name, ustr)
		return ustr

	if _tpl != None and hasattr(_tpl, '__call__'):
		func = _tpl
		_tpl = None
		return sub(func)
	return sub

class RedirectException(Exception):
	def __init__(self, url):
		self.url = url

def redirect(url, _id=None, **kwargs):
	if hasattr(url, '__call__') and hasattr(url, 'url'):
		url = url.url(_id, **kwargs)
	print 'Redirecting to', url
	raise RedirectException(url)
