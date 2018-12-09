try:
	from flask import Blueprint
	from flask_sqlalchemy import SQLAlchemy
	from flask_praetorian import Praetorian
	from flask_cors import CORS
	from flask_migrate import Migrate
	import flask_login
except ImportError as IE:
	print(f"Error importing Models Blueprint: {IE}")

# Initializes (routes) blueprint
model = Blueprint('model',__name__, None)
model.config = {}

# Sets DB Terms
db = SQLAlchemy()
guard = Praetorian()
cors = CORS()
login_manager = flask_login.LoginManager()

try:
	# Imports model Classes
	from .user import User
	from .post import Post
	from .room import Room
except Exception as e:
	print(f"Error loading models: {e}")

@model.record
def record_params(setup_state):
	"""
	Initializes DB Terms
	app amd model.config is used for accessing the app context
	"""
	app = setup_state.app
	model.config = dict([(key,value) for (key,value) in app.config.items()])
	migrate = Migrate(app, db)
	guard.init_app(app, User)
	db.init_app(app)
	cors.init_app(app)
	login_manager.init_app(app)