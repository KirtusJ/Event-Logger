try:
	from . import routes
	from flask import render_template, request
	from bin.controllers import ErrorController, UserController, RoomController
except ImportError as IE:
	print(f"Error importing in routes/rooms.py: {IE}")

@routes.route('/r/<name>/', methods=['POST', 'GET'])
def show_room(name):
	"""
	Sends name to RoomController
	function show()
	"""
	if request.method == "GET":
		return RoomController.show(name)
	else:
		return ErrorController.error("404"), 404

@routes.route('/room/new', methods=['POST', 'GET'])
@UserController.login_required
def create_room():
	"""
	Ensures current_user

	if POST
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to RoomController 
	
	if the identity of the form is create, sent to 
	function create()

	if GET
	Renders createroom template (TBD)
	"""
	if request.method == "POST":
		if request.form["room"] == "create":
			name = request.form["name"]
			description = request.form["description"]
			return RoomController.create(name,description)
	else:
		return ErrorController.error("404"), 404

@routes.route('/room/<id>/edit', methods=['POST','GET'])
@UserController.login_required
def update_room(id):
	"""
	Ensures current_user
	
	if POST
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to RoomController

	If the identity of the form is TBD, send to 
	TBD

	if GET
	Renders editroom template (TBD)
	"""
	if request.method == "POST":
		if request.form["room"] == "update":
			name = request.form["name"]
			description = request.form["description"]
			return RoomController.update(id,name,description)
	elif request.method == "GET":
		return RoomController.update_view(id)
	else:
		return ErrorController.error("404"), 404	

@routes.route('/room/<id>/subscribe/')
@UserController.login_required
def subscribe_room(id):
	"""
	These should probably be handled in room route and room controller
	Verifies current_user
	Sends room id to UserController
	function subscribe()
	"""
	return RoomController.subscribe(id)

@routes.route('/room/<id>/unsubscribe/')
@UserController.login_required
def unsubscribe_room(id):
	"""
	Verifies current_user
	Sends room id to UserController
	function subscribe()
	"""
	return RoomController.unsubscribe(id)