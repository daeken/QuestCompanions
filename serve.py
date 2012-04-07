import coffeescript, os
from flask import Flask
import handler
import handlers
from handlers import *
from model import Config, User

app = Flask(__name__)
app.debug = True
key = Config.getString('secret_key')
if key == None:
	key = os.urandom(24)
	Config.set('secret_key', ''.join('%02x' % ord(c) for c in key))
else:
	key = ''.join(chr(int(key[i:i+2], 16)) for i in xrange(0, 48, 2))
app.secret_key = key

def reroute(noId, withId):
	def sub(id=None, *args, **kwargs):
		try:
			if id == None:
				return noId(*args, **kwargs)
			else:
				return withId(id, *args, **kwargs)
		except:
			import traceback
			traceback.print_exc()
	sub.func_name = '__reroute_' + noId.func_name
	return sub

for module, sub in handler.all.items():
	for name, (method, args, rpc, (noId, withId)) in sub.items():
		if module == 'index':
			route = '/'
			trailing = True
		else:
			route = '/%s' % module
			trailing = False
		if name != 'index':
			if not trailing:
				route += '/'
			route += '%s' % name
			trailing = False

		if noId != None and withId != None:
			func = reroute(noId, withId)
		elif noId != None:
			func = noId
		else:
			func = withId

		if withId != None:
			iroute = route
			if not trailing:
				iroute += '/'
			iroute += '<int:id>'
			app.route(iroute, methods=[method])(func)

		if noId != None:
			app.route(route, methods=[method])(func)

@app.route('/favicon.ico')
def favicon():
	return file('static/favicon.ico', 'rb').read()

rpcStubTemplate = '''%s: function(%s, callback) {
	$.ajax(%r, 
		{
			success: function(data) {
				if(callback !== undefined)
					callback(data)
			}, 
			error: function() {
				if(callback !== undefined)
					callback()
			}, 
			dataType: 'json', 
			data: {csrf: $csrf, %s}, 
			type: 'POST'
		}
	)
}'''
cachedRpc = None
@app.route('/rpc.js')
def rpc():
	global cachedRpc
	if cachedRpc:
		return cachedRpc

	modules = []
	for module, sub in handler.all.items():
		module = [module]
		for name, (method, args, rpc, funcs) in sub.items():
			if not rpc:
				continue
			func = funcs[0] if funcs[0] else funcs[1]
			method = rpcStubTemplate % (
					name, ', '.join(args), 
					func.url(), 
					', '.join('%s: %s' % (arg, arg) for arg in args)
				)
			module.append(method)
		if len(module) > 1:
			modules.append(module)

	cachedRpc = 'var $rpc = {%s};' % (', '.join('%s: {%s}' % (module[0], ', '.join(module[1:])) for module in modules))
	return cachedRpc

@app.route('/scripts/<fn>')
def script(fn):
	try:
		if not fn.endswith('.js'):
			return ''

		fn = 'scripts/' + fn[:-3]
		if os.path.exists(fn + '.js'):
			return file(fn + '.js', 'rb').read()

		try:
			jstat = os.stat(fn + '.cjs').st_mtime
		except:
			jstat = None
		try:
			cstat = os.stat(fn + '.coffee').st_mtime
		except:
			cstat = None

		if jstat == None and cstat == None:
			return ''
		elif jstat != None and cstat == None or jstat > cstat:
			return file(fn + '.cjs', 'rb').read()

		source = file(fn + '.coffee', 'rb').read()

		source = coffeescript.compile(source)
		file(fn + '.cjs', 'wb').write(source)

		return source
	except:
		import traceback
		traceback.print_exc()

app.run(host='')
