try:
	from . import routes
	from flask import render_template, request
	from bin.controllers import ErrorController, CommentController, UserController
except ImportError as IE:
	print(f"Error importing in routes/comments.py: {IE}")	

@routes.route('/r/<room>/comments/<post>/comment/new', methods=['POST','GET'])
@UserController.login_required
def create_comment(room,post):
	"""
	Sends room, post, and body to CommentController
	function show()
	"""
	if request.method == "POST":
		if request.form["comment"] == "create":
			body = request.form["body"]
			return CommentController.create(room, post, body)
	else:
		return ErrorController.error("404"), 404

@routes.route('/r/<room>/comments/<post>/comment/<comment>/reply', methods=['POST','GET'])
@UserController.login_required
def reply_comment(room, post, comment):
	"""
	Sends room, post, comment, and body to CommentController
	function reply()
	"""
	if request.method == "POST":
		if request.form["comment"] == "reply":
			body = request.form["body"]
			return CommentController.reply(room, post, comment, body)
	else:
		return ErrorController.error("404"), 404

@routes.route('/r/<room>/comments/<post>/comment/<comment>', methods=['POST','GET'])
def show_comment(room, post, comment):
	"""
	Sends room, post, and comment to CommentController
	function show()
	"""
	if request.method == "GET":
		return CommentController.show(room, post, comment)
	else:
		return ErrorController.error("404"), 404