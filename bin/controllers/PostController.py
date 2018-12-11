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
	import os
	import logging
	import config
	import json
except Exception as e:
	print(f"Error importing in controllers/PostController.py: {e}")

def show(_room, _id):
	"""
	Shows the post view
	based on given ID
	"""
	try:
		room = Room.query.filter_by(name=_room).first()
	except:
		room = None
	try:
		post = Post.query.filter_by(id=_id).first()
	except:
		post = None


	return render_template("post/post.htm.j2", room=room, post=post)

def create(_title, _body, _room):
	"""
	Creates a post
	Sets the id 
	"""
	try:
		room = Room.query.filter_by(name=_room.lower()).first()
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
		logging.error(f"{e}")
		flash(u"An error has occured", 'error')
		return redirect(url_for('routes.index'))
	print(f"Post: {post.id} [created]")
	data = {'type' : 'post', 'title' : post.title, 'id' : post.id, 'body' : post.body, 'author' : [{'id' : post.author}, {'username' : post.author_username}], 
		'room' : [{'id' : post.room_id}, {'name' : post.room_name}], 'created_date' : str(post.created)
	}

	file = f"{config.api_directory}/post/{post.id}.json"
	if os.path.exists(f"{config.api_directory}/post/"):
		if not os.path.exists(file):
			open(file, "w")
			with open(file, "w") as json_file:
				json.dump(data, json_file)
	return redirect(url_for('routes.showPost',room=post.room_name,id=post.id))

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
		if current_user.id == post.get_author() or g.admin:
			try:
				db.session.delete(post)
				db.session.commit()
			except Exception as e:
				logging.error(f"{e}")
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
		if current_user.id == post.get_author() or g.admin:
			try:
				updated_title = False
				if not post.title == _title: 
					post.set_title(_title)
					updated_title = True
				updated_body = False
				if not post.body == _body:
					post.set_body(_body)
					updated_body = True
				db.session.commit()
			except Exception as e:
				logging.error(f"{e}")
				return ErrorController.error(e)
			print(f"Post: {_id} [updated]")
			flash(u"Post {id} updated".format(id=_id))
			file = f"{config.api_directory}/post/{post.id}.json"
			if os.path.exists(file) and updated_title is True or updated_body is True:
				with open (file, "rt") as fp:
					data = json.load(fp)
				if updated_title is True:
					data["title"] = post.title
				if updated_body is True:
					data["body"] = post.body
				with open(file, "wt") as json_file:
					json.dump(data, json_file)
			return redirect(url_for('routes.showPost', room=post.room_name, id=post.id))
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
		if current_user.id == post.get_author() or g.admin:
			return render_template("post/editpost.htm.j2", post=post)
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Post {id} doesn't exist".format(id=_id))
		return redirect(url_for('routes.index'))
	