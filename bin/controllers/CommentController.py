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
	from bin.models.comment import Comment
	from . import ErrorController

	from random import choice
	from string import ascii_uppercase
	import os
	import logging
	from config import api_directory
	import json
	import sys
except ImportError as IE:
	print(f"Error importing in controllers/CommentController.py: {IE}")

def create_comment(_room, _post, _body):
	try: room = Room.query.filter_by(name=_room.lower()).first()
	except: room = None

	try: post = Post.query.filter_by(id=_post).first()
	except: post = None

	if room is None:
		flash(u"Room: {room} doesn't exist".format(room=_room))
		return redirect(url_for('routes.index'))
	if post is None:
		flash(u"Post: {id} doesn't exist".format(id=_post))
		return redirect(url_for('routes.index'))
		
	try:
		comment = Comment(body=_body)
		comment.set_id(''.join(choice(ascii_uppercase) for i in range(12)))
		comment.set_author(current_user.id, current_user.username)
		comment.set_post(post.id)
	except Exception as e:
		return ErrorController.error(e)
	try:
		db.session.add(comment)
		db.session.commit()
	except Exception as e:
		return ErrorController.error(e)

	print(f"Comment: {comment.id} {comment.created}")
	data = {'type' : 'comment', 'parent' : True, 'body' : comment.body, 'author' : [{'id' : comment.author}, {'username' : comment.author_username}],
		'post' : comment.post_id, 'created_date' : str(comment.created)
	}
	file = f"{api_directory}/comment/{comment.id}.json"
	if os.path.exists(f"{api_directory}/comment/"):
		if not os.path.exists(file):
			open(file, 'w')
			with open(file, 'w') as json_file:
				json.dump(data, json_file)
	flash(u"Commented created successfully")
	return redirect(url_for('routes.showPost', room=post.room_name,id=post.id))

def show_comment(_room, _post, _comment):
	try: room = Room.query.filter_by(name=_room.lower()).first()
	except: room = None

	try: post = Post.query.filter_by(id=_post).first()
	except: post = None

	try: comment = Comment.query.filter_by(id=_comment).first()
	except: comment = None

	if room is None:
		flash(u"Room: {room} doesn't exist".format(room=_room))
		return redirect(url_for('routes.index'))
	if post is None:
		flash(u"Post: {id} doesn't exist".format(id=_post))
		return redirect(url_for('routes.index'))
	if comment is None:
		flash(u"Comment: {id} doesn't exist".format(id=_comment))
		return redirect(url_for('routes.index'))
	return render_template("comment/comment.htm.j2", room=room, post=post, comment=comment)
