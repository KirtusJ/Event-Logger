try:
	from . import routes
	from bin.controllers import IndexController, UserController
except ImportError as IE:
	print(f"Error importing in routes/index.py: {IE}")

@routes.context_processor
def init_project():
	return IndexController.init()

@routes.route('/')
@UserController.login_required
def index():
	"""
	Sends to IndexController 
	function show()
	"""
	return IndexController.show()

@routes.route('/users')
@UserController.login_required
def users():
	"""
	Sends to IndexController 
	function about()
	"""
	return IndexController.users()

@routes.route('/rooms')
@UserController.login_required
def rooms():
	"""
	Sends to IndexController
	function rooms()
	"""
	return IndexController.rooms()