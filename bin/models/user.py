try:
	from . import db, guard, cors
	from .room import Room
	from sqlalchemy.ext.hybrid import hybrid_property
	from sqlalchemy_imageattach.entity import Image, image_attachment
	from datetime import datetime
	from random import choice
	from string import ascii_uppercase
	import hashlib
except ImportError as IE:
	print(f"Error importing in models/user.py: {IE}")

class User(db.Model):
	"""
	Initializes the User Table
	Sets up the following columns
	1. The Unique User Identifier (id)
	2. The User's username (username)
	3. The User's email (email)
	4. The user's password (password)
	5. The user's roles (roles)
	6. The user's creation data (creation)
	7. The user's bio (bio)
	"""
	id = db.Column(db.String(12), unique=True, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	roles = db.Column(db.Text)
	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	bio = db.Column(db.Text)
	picture = image_attachment('ProfilePicture')

	
	default_role = "user"
	admin_role = "admin"
	banned_role = "banned"

	"""
	To be done
	1. Setting up moderators for rooms
	2. Creating the created column

	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	"""

	"""
	Initializes the Followers table
	Sets up the following columns
	1. The ID of the follower (follower_id)
	2. The ID of the user being followed (followed_id)
	Sets as unique
	"""

	followers = db.Table('followers',
		db.Column('follower_id', db.String(12), db.ForeignKey("user.id")),
		db.Column('followed_id', db.String(12), db.ForeignKey("user.id")),
		db.UniqueConstraint('follower_id', 'followed_id', name='uix_1')
	)
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
	)

	subscribed = db.relationship(
		'Room', secondary=Room.subscribers,
		primaryjoin=(Room.subscribers.c.subscriber_username == username),
		secondaryjoin=(Room.subscribers.c.subscribed_id == Room.id),
		backref=db.backref('subscribers', lazy='dynamic'), lazy='dynamic'
	)

	def __repr__(self):
		return f'<User: {self.username}>'

	def __init__(self, username, email, roles):
		""" Used for Initializing the User"""
		self.username = username
		self.email = email
		self.roles = roles
		super(User,self).__init__()

	@property
	def rolenames(self):
		try:
			return self.roles.split(',')
		except Exception:
			return []

	@classmethod
	def lookup(cls, username):
		return cls.query.filter_by(username=username).one_or_none()	

	@classmethod
	def identify(cls, id):
		return cls.query.get(id)

	@classmethod
	def is_active():
		return True

	def is_authenticated(self):
		return self.authenticated

	def set_password(self, password):
		self.password = guard.encrypt_password(password)

	def set_email(self, email):
		self.email = email

	def set_username(self, username):
		self.username = username

	def set_id(self, id):
		self.id = id

	def set_role(self, role):
		self.roles = role

	def set_bio(self, bio):
		self.bio = bio

	def check_password(self, username, password):
		return guard.authenticate(username, password)

	def get_id(self):
		return f"{self.id}"

	def follow(self, user):
		self.followed.append(user)

	def unfollow(self, user):
		self.followed.remove(user)

	def subscribe(self, room):
		self.subscribed.append(room)

	def unsubscribe(self, room):
		self.subscribed.remove(room)

class ProfilePicture(db.Model, Image):
	""" User Profile Picture"""

	user_id = db.Column(db.String(12), db.ForeignKey('user.id'), primary_key=True)
	user = db.relationship('User')

	@property
	def object_id(self):
		return int(hashlib.sha1(self.user_id.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
