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
	4. The author id of the post (author)
	5. The author username of the post (author_username)
	6. The room id of the post (room_id)
	7. The room name of the post (room_name)
	8. The time the post was created (created)
	"""
	id = db.Column(db.String(12), unique=True, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	body = db.Column(db.String(1000), nullable=False)
	author = db.Column(db.String(12), db.ForeignKey('user.id'))
	author_username = db.Column(db.String(100))
	room_id = db.Column(db.String(12), db.ForeignKey('room.id'))
	room_name = db.Column(db.String(120))
	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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

	def set_author(self, id, username):
		self.author = id 
		self.author_username = username

	def set_title(self, title):
		self.title = title

	def set_body(self, body):
		self.body = body

	def get_id(self):
		return f"{self.id}"

	def get_author(self):
		return self.author

	def set_room(self, room_id, room_name):
		self.room_id = room_id
		self.room_name = room_name

	def get_room(self):
		return self.room_id