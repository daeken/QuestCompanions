import os
from json import dumps
from flask import abort, render_template, request, session
from flask import redirect as _redirect
from werkzeug.exceptions import HTTPException
from model import User
from urllib import quote, urlencode

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class DictObject(dict):
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
			method = 'POST'
		elif name.startswith('rpc_'):
			method = 'POST'
			rpc = json = True
			tpl = None
		else:
			raise Exception('All handlers must be marked get_ or post_.')

		module = func.__module__.split('.')[-1]
		if not module in all:
			all[module] = DictObject()
			setattr(handler, module, all[module])
		args = func.__code__.co_varnames[:func.__code__.co_argcount]
		hasId = len(args) > 0 and args[0] == 'id' and not rpc

		ofunc = func
		def func(id=None):
			if 'csrf' not in session:
				token = os.urandom(16)
				session['csrf'] = ''.join('%02x' % ord(c) for c in token)
			if method == 'POST' and \
				('csrf' not in request.form or request.form['csrf'] != session['csrf']):
				abort(403)
			if 'userId' in session and session['userId']:
				session.user = User.one(id=int(session['userId']))
			else:
				session.user = None
			if (authed or admin) and session.user == None:
				return _redirect('/')
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
					ret = ofunc(int(id), **kwargs)
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
				ret['request'] = request
				ret['session'] = session
				ret['len'] = len
				ret = render_template(tpl + '.html', **ret)
				csrf = '<input type="hidden" name="csrf" value="%s">' % session['csrf']
				return ret.replace('$CSRF$', csrf)
			else:
				return ret

		func.func_name = '__%s__%s__' % (module, name)

		def url(_id=None, **kwargs):
			if module == 'index':
				url = '/'
				trailing = True
			else:
				url = '/%s' % module
				trailing = False
			if name != 'index':
				if not trailing:
					url += '/'
				url += '%s' % name
				trailing = False
			if _id != None:
				if not trailing:
					url += '/'
				url += quote(str(_id))
			if len(kwargs):
				url += '?'
				url += urlencode(dict((k, str(v)) for k, v in kwargs.items()))
			return url

		ustr = StrObject(url())
		ustr.__call__ = ofunc
		ustr.url = url
		func.url = url
		if not name in all[module]:
			all[module][name] = method, args, rpc, [None, None]
		if hasId and not rpc:
			all[module][name][3][1] = func
		else:
			all[module][name][3][0] = func
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

from jinja2 import Environment, FileSystemLoader
email_env = Environment(loader=FileSystemLoader('templates/emails'))
def email(recv, tpl, **args):
	tpl = email_env.get_template(tpl + '.html')
	def render_template(tpl, **args):
		return template.render(**args)

	html = tpl.render(html=True, handler=handler, **args)
	title, html = html.split('\n', 1)
	text = tpl.render(html=False, handler=handler, **args)
	
	msg = MIMEMultipart('alternative')
	msg['Subject'] = title
	_from = msg['From'] = 'notifications@questcompanions.com'
	msg['To'] = recv

	msg.attach(MIMEText(text, 'plain'))
	msg.attach(MIMEText(html, 'html'))

	try:
		s = smtplib.SMTP_SSL('email-smtp.us-east-1.amazonaws.com')
		s.login('AKIAJTUVTEOZ2GOXQG7A', 'Anuu9LuAauvS/DL2/V0wAYKNNedacVXlq2d+JaDSYAgB')
		s.sendmail(_from, recv, msg.as_string())
		s.quit()
		return True
	except:
		return False
