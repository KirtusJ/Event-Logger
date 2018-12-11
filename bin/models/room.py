try:
	from . import db, guard, cors
	from sqlalchemy.ext.hybrid import hybrid_property
	from random import choice
	from string import ascii_uppercase
	from datetime import datetime
except ImportError as IE:
	print(f"Error importing in models/room.py: {IE}")

class Room(db.Model):
	"""
	Initializes the Room Table
	Sets up the following columns
	1. The Unique Room Identifier (id)
	2. The name of the Room (name)
	3. The description of the Room (description)
	4. The owner id of the Room (owner)
	5. The owner username of the room (owner_username)
	6. The time the Room was created (created)
	"""
	id = db.Column(db.String(12), unique=True, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	description = db.Column(db.String(1000))
	owner = db.Column(db.String(12), db.ForeignKey('user.id'))
	owner_username = db.Column(db.String(100))
	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	subscribers = db.Table('subscribers',
		db.Column('subscriber_username', db.String(12), db.ForeignKey("user.username")),
		db.Column('subscribed_id', db.String(100), db.ForeignKey("room.id")),
		db.UniqueConstraint('subscriber_username', 'subscribed_id', name='uix_1')
	)

	"""
	To be done
	1. Setting up post relationships
	2. Adding moderators
	"""

	def __repr__(self):
		""" Used for printing self """
		return f'<Room: {self.id}>'

	def __init__(self, name, description):
		""" Used for Initializing the Room"""
		self.name = name
		self.description = description
		super(Room,self).__init__()

	@classmethod
	def lookup(cls, id):
		""" Used for looking up room by id"""
		return cls.query.filter_by(id=id).one_or_none()	

	@classmethod
	def identify(cls, id):
		""" Used for identifying room based on id"""
		return cls.query.get(id)

	@classmethod
	def is_active():
		"""
		Determines if a room is active
		Currently always true
		To be worked on more
		"""
		return True

	def set_id(self, id):
		""" Sets room id """
		self.id = id

	def set_owner(self, id, username):
		""" Sets room owner """
		self.owner = id
		self.owner_username = username

	def set_name(self, name):
		self.name = name

	def set_description(self, description):
		self.description = description

	def get_id(self):
		""" Used for returning room id as a string """
		return f"{self.id}"

	def get_owner(self):
		""" Used for returning the room owner """
		return self.owner