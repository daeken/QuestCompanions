from flask import Flask
import handler
import handlers
from handlers import *

app = Flask(__name__)

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

app.run()
