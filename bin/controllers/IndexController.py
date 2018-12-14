try:
	from flask import (
		render_template, g
	)
	from flask_login import (
		current_user
	)
	from bin.__init__ import AppClass
	from bin.models.user import User
	from bin.models.post import Post
	from bin.models.room import Room
except ImportError as IE:
	print(f"Error importing in controllers/IndexController.py: {IE}")


def init():
	return dict(project=[AppClass.project_name])

def show():
	"""
	If current_user

	Shows the index view
	Passes all posts and renders them

	If not current_user
	Shows the splash view
	"""
	if current_user.is_authenticated:
		post = Post.query.order_by(Post.created.desc()).all()
		subscribed=None
		if current_user.is_authenticated:
			for f in current_user.subscribed:
				subscribed=current_user.subscribed
		return render_template('index/index.htm.j2', users=users, posts=post, subscribed=subscribed)
	else:
		return render_template('index/splash.htm.j2')
def users():
	"""
	Shows the users view
	Passes all users and renders them
	"""
	try:
		users = User.query.order_by(User.id).all()
	except:
		users = None
	return render_template('index/users.htm.j2', users=users)

def rooms():
	"""
	Shows the rooms view
	Passes all rooms and renders them
	"""
	try:
		rooms = Room.query.order_by(Room.created.desc()).all()
	except:
		rooms = None
	return render_template('index/rooms.htm.j2', rooms=rooms)