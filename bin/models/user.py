try:
	from . import db, guard, cors
	from sqlalchemy.ext.hybrid import hybrid_property
	from datetime import datetime
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
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	roles = db.Column(db.Text)
	default_role = "user"
	admin_role = "admin"
	banned_role = "banned"

	"""
	To be done
	1. Setting up moderators for rooms
	2. Creating the created column

	#created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	"""

	"""
	Initializes the Followers table
	Sets up the following columns
	1. The ID of the follower (follower_id)
	2. The ID of the user being followed (followed_id)
	Sets as unique
	"""

	followers = db.Table('followers',
		db.Column('follower_id', db.Integer, db.ForeignKey("user.id")),
		db.Column('followed_id', db.Integer, db.ForeignKey("user.id")),
		db.UniqueConstraint('follower_id', 'followed_id', name='uix_1')
	)
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
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

	def check_password(self, username, password):
		return guard.authenticate(username, password)

	def set_role(self, role):
		self.roles = role

	def get_id(self):
		return f"{self.id}"

	def follow(self, user):
		self.followed.append(user)

	def unfollow(self, user):
		self.followed.remove(user)

