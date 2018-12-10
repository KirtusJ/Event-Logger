try:
	from flask import (
		render_template, g, redirect, url_for, flash
	)
	from flask_login import (
		current_user
	)
	from bin.models import (
		guard, db, login_manager
	)
	from bin.models.post import Post
	from bin.models.room import Room
	from . import ErrorController

	from random import choice
	from string import ascii_uppercase
	import logging
except Exception as e:
	print(f"Error importing in controllers/PostController.py: {e}")

def show(_id):
	"""
	Shows the post view
	based on given ID
	"""
	try:
		post = Post.query.filter_by(id=_id).first()
	except:
		post = None
	return render_template("post/post.htm.j2", post=post)

def create(_title, _body, _room):
	"""
	Creates a post
	Sets the id 
	"""
	try:
		room = Room.query.filter_by(name=_room).first()
	except:
		room = None
	if room is None:
		flash(u"Room: {room} doesn't exist".format(room=_room))
		return redirect(url_for('routes.showUser', username=current_user.username))
	else:
		post = Post(title=_title, body=_body)
	try:
		post.set_id(''.join(choice(ascii_uppercase) for i in range(12)))
		post.set_author(g.user.id, g.user.username)
		post.set_room(room.id, room.name)
		db.session.add(post)
		db.session.commit()
	except Exception as e:
		logging.error(f"Error: {e}")
		flash(u"An error has occured", 'error')
		return redirect(url_for('routes.index'))
	print(f"Post: {post.id} [created]")
	return redirect(url_for('routes.showPost', id=post.id))

def destroy(_id):
	"""
	Destroys a post through a given ID
	Ensures that the current_user is either the post author or g.admin 
	"""
	try:
		post = Post.query.filter_by(id=_id).first()
	except:
		post = None
	if post is not None:
		if current_user.username == post.get_author() or g.admin:
			try:
				db.session.delete(post)
				db.session.commit()
			except Exception as e:
				logging.error(f"Error: {e}")
				return ErrorController.error(e)
			print(f"Post: {_id} [deleted]")
			flash(u"Post {id} has been deleted".format(id=_id))
			return redirect(url_for('routes.index'))
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Post {id} doesn't exist".format(id=_id), 'error')
		return redirect(url_for('routes.index'))

def update(_id, _title, _body):
	"""
	Updates post
	"""
	try:
		post = Post.query.filter_by(id=_id).first()
	except:
		post = None
	if post is not None:
		if current_user.username == post.get_author() or g.admin:
			try:
				if not post.title == _title: 
					post.set_title(_title)
				if not post.body == _body:
					post.set_body(_body)
				db.session.commit()
			except Exception as e:
				logging.error(f"Error: {e}")
				return ErrorController.error(e)
			print(f"Post: {_id} [updated]")
			flash(u"Post {id} updated".format(id=_id))
			return redirect(url_for('routes.showPost', id=post.id))
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Post {id} doesn't exist".format(id=_id))
		return redirect(url_for('routes.index'))

def updateView(_id):
	try:
		post = Post.query.filter_by(id=_id).first()
	except:
		post = None
	if post is not None:
		if current_user.username == post.get_author() or g.admin:
			return render_template("post/editpost.htm.j2", post=post)
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Post {id} doesn't exist".format(id=_id))
		return redirect(url_for('routes.index'))
	