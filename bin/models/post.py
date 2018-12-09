try:
	from . import db, guard, cors
	from sqlalchemy.ext.hybrid import hybrid_property
	from random import choice
	from string import ascii_uppercase
	from datetime import datetime
except ImportError as IE:
	print(f"Error importing in models/post.py: {IE}")

class Post(db.Model):
	"""
	Initializes the Post Table
	Sets up the following columns
	1. The Unique Post Identifier (id)
	2. The Post Title (title)
	3. The content of the Post (body)
	4. The author of the post (post_author)
	5. The time the post was created (created)
	"""
	id = db.Column(db.String(12), unique=True, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	body = db.Column(db.String(1000), nullable=False)
	post_author = db.Column(db.String(100), db.ForeignKey('user.username'))
	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	"""
	To be done
	1. Setting up room relationships
	
	room_id = db.Column(db.String(12), db.ForeignKey('room.id'))
	room = db.relationship('Room', backref-db.backref('posts', lazy=True))
	"""

	def __repr__(self):
		return f'<Post: {self.id}>'

	def __init__(self, title, body):
		""" Used for Initializing the Post"""
		self.title = title
		self.body = body
		super(Post,self).__init__()

	@classmethod
	def lookup(cls, id):
		return cls.query.filter_by(id=id).one_or_none()	

	@classmethod
	def identify(cls, id):
		return cls.query.get(id)

	@classmethod
	def is_active():
		return True

	def set_id(self, id):
		self.id = id

	def set_author(self, username):
		self.post_author = username

	def set_title(self, title):
		self.title = title

	def set_body(self, body):
		self.body = body

	def get_id(self):
		return f"{self.id}"

	def get_author(self):
		return self.post_author