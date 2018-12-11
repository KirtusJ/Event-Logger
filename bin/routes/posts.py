try:
	from . import routes
	import flask
	from flask import render_template
	from bin.controllers import ErrorController, PostController, UserController
	from flask_login import current_user
except ImportError as IE:
	print(f"Error importing in routes/posts.py: {IE}")	

@routes.route('/post/new', methods=['POST', 'GET'])
@UserController.login_required
def createPost():
	"""
	Varifies current_user
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to PostController 
	function create()
	"""
	if flask.request.method == "POST":
		if flask.request.form["post"] == "create":
			title = flask.request.form["title"]
			body = flask.request.form["body"]
			room = flask.request.form["room"]
			return PostController.create(title, body, room)
	else:
		return ErrorController.error("404"), 404

@routes.route('/post/<id>/delete/')
@UserController.login_required
def destroyPost(id):
	"""
	Verifies current_user
	Sends post id to PostController 
	function destroy()
	"""
	return PostController.destroy(id)

@routes.route('/r/<room>/comments/<id>/')
def showPost(room, id):
	"""
	Sends post id to PostController 
	function show()
	"""
	return PostController.show(room, id)

@routes.route('/post/<id>/edit', methods=['GET','POST'])
@UserController.login_required
def updatePost(id):
	"""
	Verifies current_user

	if POST
	Sends post id to PostController
	function update()

	if GET
	Sends post id to PostController
	function updateView()
	"""
	if flask.request.method == "POST":
		if flask.request.form["post"] == "update":
			title = flask.request.form["title"]
			body = flask.request.form["body"]
			return PostController.update(id, title, body)
	elif flask.request.method == "GET":
		return PostController.updateView(id)
	else:
		return ErrorController.error("404"), 404
