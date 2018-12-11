try:
	from flask import (
		render_template, g, redirect, url_for, flash
	)
	from flask_login import (
		current_user
	)
	from bin.models import (
		db
	)
	from bin.models.user import User
	from bin.models.post import Post
	from bin.models.room import Room
	from . import ErrorController
	
	from random import choice
	from string import ascii_uppercase
	import logging
	from config import api_directory
	import json
	import os
except Exception as e:
	print(f"Error importing in controllers/RoomController.py: {e}")

def show(_name):
	""" 
	Shows specified room 
	Example: /r/<name>
	Will render this room
	"""
	try:
		room = Room.query.filter_by(name=_name).first()
	except:
		room = None
	try:
		posts = Post.query.filter_by(room_id=room.id).all()
	except:
		posts = None

	subscribers=None
	is_subscribed=None
	for s in room.subscribers:
		subscribers=room.subscribers
		if current_user.is_authenticated and current_user.username == s.username:
			is_subscribed=True
			break

	return render_template("room/room.htm.j2", room=room, posts=posts, subscribers=subscribers, is_subscribed=is_subscribed)

def create(_name, _description):
	"""
	Creates a room if all criteria is met
	If the route has arrived here, the user has already been authenticated
	1. Room name doesn't exist
	"""
	try:
		roomname = Room.query.filter_by(name=_name).first()
	except:
		roomname = None
	if roomname is not None:
		flash(u"Room {name} already exists".format(name=_name), 'error')
		return render_template('index/rooms.htm.j2')
	try:
		room = Room(name=_name.lower(), description=_description)
		room.set_owner(g.user.id, g.user.username)
		room.set_id(''.join(choice(ascii_uppercase) for i in range(12)))
		db.session.add(room)
		current_user.subscribe(room)
		db.session.commit()
	except Exception as e:
		logging.error(f"{e}")
		flash(u"An error has occured", 'error')
		return render_template('index/index.htm.j2')
	print(f"Room: {room.name} [created]")
	data = {'type' : 'room', 'name' : room.name, 'id' : room.id, 'description' : room.description, 'owner' : [{'id' : room.owner}, {'username' : room.owner_username}], 
		'created_date' : str(room.created)
	}
	file = f"{api_directory}/room/{room.id}.json"
	if os.path.exists(f"{api_directory}/room/"):
		if not os.path.exists(file):
			open(file, "w")
			with open(file, "w") as json_file:
				json.dump(data, json_file)
	return redirect(url_for('routes.showRoom', name=room.name))

def destroy(_name):
	"""
	Deletes a room if said room exists
	Authenticates that current_user is either the owner of the room or an admin
	"""
	try:
		room = Room.query.filter_by(name=_name).first()
	except:
		room = None
	if room is not None:
		if current_user.id == room.get_owner() or g.admin:
			try:
				db.session.delete(room)
				db.session.commit()
			except Exception as e:
				logging.error(f"{e}")
				return ErrorController.error(e)
			print(f"Room: {_name} [deleted]")
			flash(u"Room {name} has been deleted".format(name=_name))
			return redirect(url_for('routes.index'))
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Room {name} doesn't exist".format(name=_name), 'error')
		return redirect(url_for('routes.index'))

def update(_id, _name, _description):
	"""
	Updates post
	"""
	try:
		room = Room.query.filter_by(id=_id).first()
	except:
		room = None
	if room is not None:
		if current_user.id == room.get_owner() or g.admin:
			try:
				updated_name = False
				if not room.name == _name: 
					posts = Post.query.filter_by(room_id=room.id).all()
					for post in posts:
						try:
							post.set_room(room.id, _name.lower())
						except Exception as e:
							logging.error(f"Error: {e}")
							return ErrorController.error(e)
					room.set_name(_name.lower())
					updated_name = True
				updated_description = False
				if not room.description == _description:
					room.set_description(_description)
					updated_description = True
				db.session.commit()
			except Exception as e:
				logging.error(f"{e}")
				return ErrorController.error(e)
			print(f"Room: {_id} [updated]")
			flash(u"Room {id} updated".format(id=_id))
			file = f"{api_directory}/room/{room.id}.json"
			if os.path.exists(file) and updated_name is True or updated_description is True:
				with open (file, "rt") as fp:
					data = json.load(fp)
				if updated_name is True:
					data["name"] = room.name
				if updated_description is True:
					data["description"] = room.description
				with open(file, "wt") as json_file:
					json.dump(data, json_file)
			return redirect(url_for('routes.showRoom', name=room.name))
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Room {id} doesn't exist".format(id=_id))
		return redirect(url_for('routes.index'))

def updateView(_id):
	try:
		room = Room.query.filter_by(id=_id).first()
	except:
		room = None
	if room is not None:
		if current_user.id == room.get_owner() or g.admin:
			return render_template("room/editroom.htm.j2", room=room)
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Room {id} doesn't exist".format(id=_id))
		return redirect(url_for('routes.index'))
	
