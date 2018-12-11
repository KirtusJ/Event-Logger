try:
	from flask import (
		render_template, g, redirect, url_for, flash
	)
	from bin.models import (
		db, login_manager
	)
	from flask_login import (
		login_user, logout_user, current_user
	)
	from bin.models.user import User
	from bin.models.post import Post
	from bin.models.room import Room
	from . import ErrorController

	from random import choice
	from string import ascii_uppercase
	import logging
	import functools
	import os
	from config import api_directory
	import json
except Exception as e:
	print(f"Error importing in controllers/UserController.py: {e}")

""" Work on naming conventions """

@login_manager.user_loader
def user_loader(user_id):
	""" Loads current_user """
	return User.query.get(user_id)

def login_required(view):
	""" Used for authenticating if a user is logged in """
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if current_user is None:
			return redirect(url_for('routes/login'))
		return view(**kwargs)
	return wrapped_view

def admin_required(view):
	""" Used for authenticating if a user is an admin """
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if not current_user.is_authenticated:
			return ErrorController.error("404"), 404
		if not g.admin:
			return ErrorController.error("404"), 404
		return view(**kwargs)
	return wrapped_view

def show(_username):
	""" 
	Shows specified user profile 
	Example: /u/<username>
	Will render this users profile
	"""
	try:
		# An exception is passed if user is null
		user = User.query.filter_by(username=_username).first()
	except:
		user=None
	try:
		# An exception is passed if posts is null
		posts = Post.query.filter_by(author=user.id).all()
	except:
		posts = None
	try:
		owned_rooms = Room.query.filter_by(owner=user.id).all()
	except:
		owned_rooms = None

	# Needed in case it is impossible to pass into the for loops
	is_following=None
	followers=None
	followed=None
	subscribed=None

	if user is not None:
		for f in user.followers:
			followers=user.followers
			if current_user.is_authenticated and current_user.id == f.id: 
				is_following=True
				break
		for f in user.followed:
			followed=user.followed
		for f in user.subscribed:
			subscribed = user.subscribed


	return render_template("user/profile.htm.j2", user=user, posts=posts, followers=followers, is_following=is_following, followed=followed, subscribed=subscribed, owned_rooms=owned_rooms)

def login(_username, _password):
	"""
	Logs in specified user if all criteria is met
	1. User exists
	2. Password is correct
	3. Is not banned
	"""
	try:
		user = User.query.filter_by(username=_username).first()
	except:
		user = None
	if user is None:
		flash(u"Username {name} doesn't exist".format(name=_username), 'error')
		return redirect(url_for('routes.createSessionView'))
	try:
		if user.check_password(_username, _password):
			if "banned" in user.roles:
				flash(u'Account {name} has been banned'.format(name=_username), 'error')
				return redirect(url_for('routes.createSessionView'))
			try:
				login_user(user)
			except Exception as e:
				logging.error(f"Error: {e}")
				return ErrorController.error(e)
			print(f"User: {user.username} [logged in]")
			return redirect(url_for('routes.index'))
	except:
		flash(u'Incorrect password', 'error')
		return redirect(url_for('routes.createSessionView'))

def register(_username, _email, _password):
	"""
	Registers a user if all criteria is met
	1. User doesn't exist
	2. Email is not in use
	"""
	username = User.query.filter_by(username=_username).first()
	email = User.query.filter_by(email=_email).first()
	if email is not None:
		flash(u'Email {email} is already in use'.format(email=_email), 'error')
		return redirect(url_for('routes.createUserView'))
	if username is not None:
		flash(u'Username {name} already exists'.format(name=_username), 'error')
		return redirect(url_for('routes.createUserView'))
	try:
		user = User(username=_username, email=_email, roles=f"{User.default_role}")
		user.set_password(_password)
		user.set_id(''.join(choice(ascii_uppercase) for i in range(12)))
	except Exception as e:
		logging.error(f"Error: {e}")
		return ErrorController.error(e)
	db.session.add(user)
	db.session.commit()
	print(f"User: {user.username} [registered]")
	flash(u"User {name} has been created".format(name=_username))

	data = {'type' : 'user', 'username' : user.username, 'id' : user.id, 'email' : user.email, 'roles' : user.roles, 'created_date' : str(user.created), 'bio' : None}
	file = f"{api_directory}/user/{user.id}.json"
	if os.path.exists(f"{api_directory}/user/"):
		if not os.path.exists(file):
			open(file, "w")
			with open(file, "w") as json_file:
				json.dump(data, json_file)

	return redirect(url_for('routes.createSessionView'))

def logout():
	"""
	Logs out current_user
	If a session exists
	"""
	try:
		if current_user.is_authenticated:
			flash(u"User {name} logged out".format(name=current_user.username))
			print(f"User: {current_user.username} [logged out]")
			logout_user()
		else:
			return redirect(url_for('routes.index'))
	except Exception as e:
		logging.error(f"Error: {e}")
		return ErrorController.error(e)
	return redirect(url_for('routes.index'))

def ban(_username):
	"""
	Handles the banning and unbanning of a user
	If the route has arrived here, the user has already been authenticated
	"""
	try:
		user = User.query.filter_by(username=_username).first()
	except:
		user = None
	if user is None:
		flash(u"User doesn't exist", 'error')
		return redirect(url_for('routes.index'))
	if "banned" not in user.roles:
		try:
			user.set_role(f"{user.roles}, {User.banned_role}")
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			logging.error(f"Error: {e}")
			return ErrorController.error(e)
		print(f"User: {user.username} [banned]")
		flash(u"User has been banned")
	elif "banned" in user.roles:
		try:
			roleList = user.roles.split(", banned")
			roleString = ''.join(roleList)
			user.set_role(roleString)
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			logging.error(f"Error: {e}")
			return ErrorController.error(e)
		print(f"User: {user.username} [unbanned]")
		flash(u"User has been unbanned")

	file = f"{api_directory}/user/{user.id}.json"
	if os.path.exists(file):
		with open (file, "rt") as fp:
			data = json.load(fp)
		data["roles"] = user.roles
		with open(file, "wt") as json_file:
			json.dump(data, json_file)
	return redirect(url_for("routes.showUser", username=user.username))

def destroy(_username):
	"""
	Deletes a user if said user exists
	If the route has arrived here, the user has already been authenticated
	"""
	try:
		user = User.query.filter_by(username=_username).first()
	except:
		user = None
	if user is None:
		flash(u"User doesn't exist", 'error')
		return redirect(url_for('routes.index'))
	try:
		db.session.delete(user)
		db.session.commit()
	except Exception as e:
		logging.error(f"Error: {e}")
		return ErrorController.error(e)
	print(f"User: {_username} [deleted]")
	flash(u"User {name} has been deleted".format(name=_usernamea))
	return redirect(url_for('routes.index'))

def follow(_username):
	"""
	Adds a followed specified_user to current_user
	Adds a follower from current_user to specified_user
	"""
	try:
		user = User.query.filter_by(username=_username).first()
	except:
		user = None
	if user is not None:
		try:
			current_user.follow(user)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			logging.error(f"{e}")
			return ErrorController.error(e)
		return redirect(url_for("routes.showUser", username=user.username))
	flash(u"User: {username} doesn't exist".format(username=_username))
	return redirect(url_for("routes.index"))

def unfollow(_username):
	"""
	Removes a followed specified_user to current_user
	Removes a follower from current_user to specified_user
	"""
	try:
		user = User.query.filter_by(username=_username).first()
	except:
		user = None
	if user is not None:
		try:
			current_user.unfollow(user)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			logging.error(f"{e}")
			return ErrorController.error(e)
		return redirect(url_for("routes.showUser", username=user.username))
	flash(u"User: {username} doesn't exist".format(username=_username))
	return redirect(url_for("routes.index"))

def subscribe(_id):
	"""
	Adds a subscription to specified_room by current_user
	Adds a subscriber to specified_room by current_user
	"""
	try:
		room = Room.query.filter_by(id=_id).first()
	except Exception as e:
		room = None
	if room is not None:
		try:
			current_user.subscribe(room)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			logging.error(f"{e}")
			return ErrorController.error(e)
		return redirect(url_for("routes.showRoom", name=room.name))
	flash(u"Room: {id} doesn't exist".format(id=_id))
	return redirect(url_for("routes.index"))

def unsubscribe(_id):
	"""
	Removes a subscription to specified_room by current_user
	Removes a subscriber to specified_room by current_user
	"""
	try:
		room = Room.query.filter_by(id=_id).first()
	except:
		room = None
	if room is not None:
		try:
			current_user.unsubscribe(room)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			logging.error(f"{e}")
			return ErrorController.error(e)
		return redirect(url_for("routes.showRoom", name=room.name))
	flash(u"Room: {id} doesn't exist".format(id=_id))
	return redirect(url_for("routes.index"))

def getUser():
	"""
	Sets global user variables
	If current_user exists, g.user does
	If current_user is an admin, g.admin is True
	"""
	if current_user.is_authenticated:
		g.user = current_user
		if "admin" in g.user.roles:
			g.admin = True
		else:
			g.admin = False
	else:
		g.user = None

def update(_username, _email, _bio, _password):
	"""
	Used to update user data
	Authenticates user password given
	Updates if:
	1. Password authenticates
	2. Username given is not in use
	3. Email given is not in use
	4. Information given is different than previous value
	"""
	try:
		current_user.check_password(current_user.username, _password)
	except Exception as e:
		flash(u"Incorrect password")
		return redirect(url_for("routes.updateUser"))
	try:
		updated_username = False
		if not current_user.username == _username: 
			username = User.query.filter_by(username=_username).first()
			if username is not None:
				flash(u'Username: {username} already in use'.format(username=_username))
				return redirect(url_for('routes.updateUser'))
			posts = Post.query.filter_by(author=current_user.id).all()
			for post in posts:
				try:
					post.set_author(current_user.id, _username)
				except Exception as e:
					logging.error(f"Error: {e}")
					return ErrorController.error(e)
			current_user.set_username(_username)
			updated_username = True
		updated_email = False
		if not current_user.email == _email:
			email = User.query.filter_by(email=_email).first()
			if email is not None:
				flash(u'Email: {email} already in use'.format(email=_email))
				return redirect(url_for("routes.updateUser"))
			try:
				current_user.set_email(_email)
				updated_email = True
			except Exception as e:
				logging.error(f"{e}")
				return ErrorController.error(e)
		updated_bio = False
		if not current_user.bio == _bio:
			try:
				current_user.set_bio(_bio)
				updated_bio = True
			except Exception as e:
				logging.error(f"{e}")
				return ErrorController.error(e)
		try:
			db.session.commit()
		except Exception as e:
			logging.error(f"{e}")
			return ErrorController.error(e)
	except Exception as e:
		logging.error(f"{e}")
		return ErrorController.error(e)
	print(f"User: {_username} [updated]")
	flash(u"Profile updated")
	file = f"{api_directory}/user/{current_user.id}.json"
	if os.path.exists(file) and updated_username is True or updated_email is True or updated_bio is True:
		with open (file, "rt") as fp:
			data = json.load(fp)
		if updated_username is True:
			data["username"] = current_user.username
		if updated_email is True:
			data["email"] = current_user.email
		if updated_bio is True:
			data["bio"] = current_user.bio
		with open(file, "wt") as json_file:
			json.dump(data, json_file)
	return redirect(url_for('routes.showUser', username=current_user.username))
def updateView():
	if not current_user.is_authenticated:
		return redirect(url_for('routes.createSessionView'))
	return render_template("user/edituser.htm.j2", user=current_user)