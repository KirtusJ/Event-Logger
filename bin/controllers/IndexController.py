try:
	from flask import (
		render_template
	)
	from flask_login import (
		current_user
	)
	from bin.models.user import User
	from bin.models.post import Post
	from bin.models.room import Room
except Exception as e:
	print(f"Error importing in controllers/IndexController.py: {e}")

def show():
	"""
	Shows the index view
	Passes all posts and renders them
	"""

	post = Post.query.order_by(Post.created.desc()).all()
	followed=None
	posts=None
	try:
		posts = Post.query.order_by(Post.created.desc()).all()
		for f in current_user.followed:
			followed=current_user.followed
	except:
		posts = post

	return render_template('index/index.htm.j2', users=users, posts=posts, followed=followed)
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