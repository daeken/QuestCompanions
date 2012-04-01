import coffeescript, os
from flask import Flask
import handler
import handlers
from handlers import *
from model import Config, User

app = Flask(__name__)
key = Config.getString('secret_key')
if key == None:
	key = os.urandom(24)
	Config.set('secret_key', ''.join('%02x' % ord(c) for c in key))
else:
	key = ''.join(chr(int(key[i:i+2], 16)) for i in xrange(0, 48, 2))
app.secret_key = key

for module, sub in handler.all.items():
	for name, (method, args, func) in sub.items():
		if module == 'index':
			route = '/'
		else:
			route = '/%s/' % module
		if name != 'index':
			route += '%s/' % name
		if len(args) and args[0] == 'id':
			route += '<id>'
		app.route(route, methods=[method])(func)

@app.route('/favicon.ico')
def favicon():
	return file('static/favicon.ico', 'rb').read()

@app.route('/scripts/<fn>')
def script(fn):
	if not fn.endswith('.js'):
		return ''

	fn = 'scripts/' + fn[:-3]
	if os.path.exists(fn + '.js'):
		return file(fn + '.js,' 'rb').read()

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

app.run()
