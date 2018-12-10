try:
	from . import routes
	import flask
	from flask import render_template
	from bin.controllers import ErrorController, UserController
	from flask_login import current_user
except ImportError as IE:
	print(f"Error importing in routes/users.py: {IE}")

@routes.before_app_request
def load_logged_in_user():
	"""
	Before any request
	Sends to UserController
	function getUser()
	"""
	return UserController.getUser()

@routes.route('/u/<username>/')
def showUser(username):
	"""
	Sends username to UserController
	function show()
	"""
	return UserController.show(username)

@routes.route('/register')
@routes.route('/signup')
def createUserView():
	""" Renders the register template """
	return render_template('user/register.htm.j2')

@routes.route('/login')
@routes.route('/signin')
def createSessionView():
	""" Renders the login template """
	return render_template('user/login.htm.j2')

@routes.route('/logout')
@UserController.login_required
def destroySession():
	"""
	Varifies current_user
	Sends to UserController
	function logout()
	"""
	return UserController.logout()

@routes.route('/auth', methods=['POST', 'GET'])
def createSessionOrUser():
	"""
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to UserController 
	
	if the identity of the form is register, sent to 
	function create()

	if the identity of the form is login, sent to
	function login()
	"""
	if flask.request.method == "POST":
		if not current_user.is_authenticated:
			if flask.request.form["auth"] == "register":
				username = flask.request.form["username"]
				email = flask.request.form["email"]
				password = flask.request.form["password"]
				return UserController.register(username,email,password)
			elif flask.request.form["auth"] == "login":
				username = flask.request.form["username"]
				password = flask.request.form["password"]
				return UserController.login(username,password)
		else:
			return ErrorController.error("403"), 403
	else:
		return ErrorController.error("404"), 404

@routes.route('/u/<username>/ban/')
@UserController.admin_required
def banUser(username):
	"""
	Verifies current_user is admin
	Sends username to UserController
	function ban()
	"""
	return UserController.ban(username)

@routes.route('/u/<username>/follow/')
@UserController.login_required
def followUser(username):
	"""
	Verifies current_user
	Sends username to UserController
	function follow()
	"""
	return UserController.follow(username)

@routes.route('/u/<username>/unfollow/')
@UserController.login_required
def unfollowUser(username):
	"""
	Verifies current_user
	Sends username to UserController
	function unfollow()
	"""
	return UserController.unfollow(username)

@routes.route('/user/edit', methods=['GET','POST'])
@UserController.login_required
def updateUser():
	"""
	Verifies current_user
	
	If POST
	Sends the user to UserController
	function update()

	If GET
	Renders the (edituser) view

	TO BE DONE
	"""
	if flask.request.method == "POST":
		if flask.request.form["user"] == "update":
			username = flask.request.form["username"]
			email = flask.request.form["email"]
			password = flask.request.form["password"]
			return UserController.update(username,email,password)
	elif flask.request.method == "GET":
		return UserController.updateView()
	else:
		return ErrorController.error("404"), 404

@routes.route('/admin/')
@UserController.admin_required
def admin():
	"""
	Verifies current_user is admin
	Currently just appends "admin"
	Plan to send to AdminController
	function show()
	"""
	return "admin"
