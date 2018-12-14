try:
	from . import routes
	from flask import render_template, request
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
	return UserController.get()

@routes.route('/u/<username>/')
@UserController.login_required
def show_user(username):
	"""
	Sends username to UserController
	function show()
	"""
	return UserController.show(username)

@routes.route('/register')
@routes.route('/signup')
def create_user_view():
	""" Renders the register template """
	return render_template('user/register.htm.j2')

@routes.route('/login')
@routes.route('/signin')
def create_user_session_view():
	""" Renders the login template """
	return render_template('user/login.htm.j2')

@routes.route('/logout')
@UserController.login_required
def destroy_user_session():
	"""
	Varifies current_user
	Sends to UserController
	function logout()
	"""
	return UserController.destroy_session()

@routes.route('/auth', methods=['POST', 'GET'])
def create_session_or_user():
	"""
	Acquires form method, and identity of the form
	If the form validates, its values will be sent to UserController 
	
	if the identity of the form is register, sent to 
	function create()

	if the identity of the form is login, sent to
	function login()
	"""
	if request.method == "POST":
		if not current_user.is_authenticated:
			if request.form["auth"] == "register":
				username = request.form["username"]
				email = request.form["email"]
				password = request.form["password"]
				return UserController.create_user(username,email,password)
			elif request.form["auth"] == "login":
				username = request.form["username"]
				password = request.form["password"]
				return UserController.create_session(username,password)
		else:
			return ErrorController.error("403"), 403
	else:
		return ErrorController.error("404"), 404

@routes.route('/u/<username>/ban/')
@UserController.admin_required
def ban_user(username):
	"""
	Verifies current_user is admin
	Sends username to UserController
	function ban()
	"""
	return UserController.ban(username)

@routes.route('/u/<username>/follow/')
@UserController.login_required
def follow_user(username):
	"""
	Verifies current_user
	Sends username to UserController
	function follow()
	"""
	return UserController.follow(username)

@routes.route('/u/<username>/unfollow/')
@UserController.login_required
def unfollow_user(username):
	"""
	Verifies current_user
	Sends username to UserController
	function unfollow()
	"""
	return UserController.unfollow(username)

@routes.route('/user/edit', methods=['GET','POST'])
@UserController.login_required
def update_user():
	"""
	Verifies current_user
	
	If POST
	Sends username, email, and password to UserController
	function update()

	If GET
	Sends the user to UserController
	function updateView()

	"""
	if request.method == "POST":
		if request.form["user"] == "update":
			username = request.form["username"]
			email = request.form["email"]
			bio = request.form["bio"]
			password = request.form["password"]
			return UserController.update(username,email,bio,password)
		else:
			profile_picture = request.files["file"]
			return UserController.update_profile_picture(profile_picture)
	elif request.method == "GET":
		return UserController.update_view()
	else:
		return ErrorController.error("404"), 404
