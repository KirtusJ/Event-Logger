try:
	from . import routes
	from flask import render_template, request
	from bin.controllers import ErrorController, PostController, UserController
except ImportError as IE:
	print(f"Error importing in routes/posts.py: {IE}")	

@routes.route('/post/new', methods=['POST', 'GET'])
@UserController.login_required
def create_post():
	"""
	Varifies current_user
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to PostController 
	function create()
	"""
	if request.method == "POST":
		if request.form["post"] == "create":
			title = request.form["title"]
			body = request.form["body"]
			room = request.form["room"]
			return PostController.create(title, body, room)
	else:
		return ErrorController.error("404"), 404

@routes.route('/post/<id>/delete/')
@UserController.login_required
def destroy_post(id):
	"""
	Verifies current_user
	Sends post id to PostController 
	function destroy()
	"""
	return PostController.destroy(id)

@routes.route('/r/<room>/comments/<id>/')
def show_post(room, id):
	"""
	Sends post id to PostController 
	function show()
	"""
	return PostController.show(room, id)

@routes.route('/post/<id>/edit', methods=['GET','POST'])
@UserController.login_required
def update_post(id):
	"""
	Verifies current_user

	if POST
	Sends post id to PostController
	function update()

	if GET
	Sends post id to PostController
	function updateView()
	"""
	if request.method == "POST":
		if request.form["post"] == "update":
			title = request.form["title"]
			body = request.form["body"]
			return PostController.update(id, title, body)
	elif request.method == "GET":
		return PostController.update_view(id)
	else:
		return ErrorController.error("404"), 404
