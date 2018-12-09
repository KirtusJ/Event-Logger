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
	return render_template("room/room.htm.j2", room=room)

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
		room = Room(name=_name, description=_description)
		room.set_owner(g.user.username)
		room.set_id(''.join(choice(ascii_uppercase) for i in range(12)))
	except:
		flash(u"An error has occured", 'error')
		return render_template('index.rooms.htm.j2')
	db.session.add(room)
	db.session.commit()
	print(f"Room: {room.name} [created]")
	return redirect(url_for('routes.showRoom', name=_name))

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
		if current_user == room.get_owner() or g.admin:
			db.session.delete(room)
			db.session.commit()
			print(f"Room: {_name} [deleted]")
			flash(u"Room {name} has been deleted".format(name=_name))
			return redirect(url_for('routes.index'))
		else:
			return ErrorController.error("403"), 403
	else:
		flash(u"Room {name} doesn't exist".format(name=_name), 'error')
		return redirect(url_for('routes.index'))