try:
	from flask import Blueprint
except ImportError as IE:
	print(f"Error importing Routes Blueprint: {IE}")

# Initializes (routes) blueprint
routes = Blueprint('routes',__name__)

try:
	# Imports routes
	from . import index, users, posts, rooms, comments
except Exception as e:
	print(f"Error loading routes: {e}")