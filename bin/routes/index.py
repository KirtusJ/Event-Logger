try:
	from . import routes
	from bin.controllers import IndexController
except ImportError as IE:
	print(f"Error importing in routes/index.py: {IE}")

@routes.route('/index')
@routes.route('/home')
@routes.route('/')
def index():
	"""
	Sends to IndexController 
	function show()
	"""
	return IndexController.show()

@routes.route('/users')
def users():
	"""
	Sends to IndexController 
	function about()
	"""
	return IndexController.users()

@routes.route('/rooms')
def rooms():
	"""
	Sends to IndexController
	function rooms()
	"""
	return IndexController.rooms()