try:
	from . import routes
	import flask
	from flask import render_template
	from bin.controllers import ErrorController, UserController, RoomController
	from flask_login import current_user
except ImportError as IE:
	print(f"Error importing in routes/rooms.py: {IE}")

@routes.route('/r/<name>/')
def showRoom(name):
	"""
	Sends name to RoomController
	function show()
	"""
	return RoomController.show(name)

@routes.route('/room/new', methods=['POST', 'GET'])
@UserController.login_required
def createRoom():
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
	if flask.request.method == "POST":
		if flask.request.form["room"] == "create":
			name = flask.request.form["name"]
			description = flask.request.form["description"]
			return RoomController.create(name,description)
		else:
			return "fish"
			# return render_template("room/createroom.htm.j2")
	else:
		return ErrorController.error("404"), 404

@routes.route('/room/<name>/edit', methods=['POST','GET'])
@UserController.login_required
def updateRoom(name):
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
	if flask.request.method == "POST":
		# form handling here
		return "TBD: post"
	elif flask.request.method == "GET":
		# return render_template("room/editroom.htm.j2")
		return "TBD: get"
	else:
		return ErrorController.error("404"), 404	