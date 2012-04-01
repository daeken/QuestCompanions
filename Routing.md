Routing and You
===============

Example file, `handlers/echo.py`:

	from handler import handler

	@handler
	def get_index(id, bar=None):
		return 'foo %r %r' % (id, bar)


This will create a route for `/echo/<id>` that takes an optional GET parameter called `bar`.  Hitting `/echo/blah?bar=baz` will return: `foo u'blah' u'baz'`.  Note the unicode strings.

Dear Flask, it's me, Cody
-------------------------

If you are modifying data, make sure you start your function name with `post_` rather than `get_`.  This enforces the POST method and will require a CSRF token.

How the route was won
---------------------

Routes are generated based on handler module name and method name.  The code for this is really straightforward:

	if module == 'index':
		route = '/'
	else:
		route = '/%s/' % module
	if name != 'index':
		route += '%s/' % name
	if len(args) and args[0] == 'id':
		route += '<id>'


So that means that a handler module named `index.py` is the very root of the web app.  A method named `index` (GET or POST -- you *can* have both if it makes sense!) is the root of a given handler.  So the application's handler for `/` is a method named `get_index` in a handler module named `index.py`.  Got it?  Good.

The `id` argument must be the first to the function if you want to have it.  This is handy for URLs like `/user/55`.  All non-id arguments are *optional*.  Handle their non-existence or perish.
