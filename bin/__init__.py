import os

if not os.path.isfile("config.py"):
    open("config.py", "w") 

try:
    import config
    from flask import Flask
    from bin.routes import routes
    from bin.models import model, db
    from bin.controllers import ErrorController as EC
    import pymysql
    pymysql.install_as_MySQLdb()
    import logging
    from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
except ImportError as IE:
    print(f"Error importing in __init__.py: {IE}")

# Handles http error codes
def http_error(e):
    return EC.error(e), e.code

class AppClass():
    app = Flask(__name__, instance_relative_config=True)
    ip = config.ip
    port = config.port
    host = config.host
    project_name = config.project_name
    try:
        store = HttpExposedFileSystemStore(
            path='bin/static/img/',
            prefix='static/img/',
            host_url_getter=lambda:
                AppClass.host
        )
    except Exception as e:
        print(f"Error initializing store. Probably forgot to setup config.py. {e}")

def create_app():
    """
    Creates and configures the Flask App
    1. Initializes Database Configs
    2. Initializes the Logging file
    3. Initializes Error handlers
    4. Initializes Blueprints
    5. Creates the Database if it doesn't already exist
    """

    app = AppClass.app
    try:
        app.config.from_mapping(
            SECRET_KEY=config.secret_key,
            SQLALCHEMY_DATABASE_URI=config.db_link,
            SQLALCHEMY_TRACK_MODIFICATIONS=config.db_track,
            JWT_ACCESS_LIFESPAN=config.jwt_access,
            JWT_REFRESH_LIFESPAN=config.jwt_refresh
        )
    except:
        print("Config file not configured or configured incorrectly")

    # Defines the logging file, mode, and format
    try:
        logging.basicConfig(filename=config.logging_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    except:
        print("Config file not configured or configured incorrectly")

    # Catch http error codes
    try:
        """
        To be done
        Adding more error codes
        """
        for error in (400,401,403,404,405,429,500):
            app.register_error_handler(error, http_error)
    except Exception as e:
        print(f"Error registering handler: {e}")

    # Registers blueprints
    try:
        app.register_blueprint(routes)
        app.register_blueprint(model)
    except Exception as e:
        print(f"Error registering blueprint: {e}")

    # Creates databasse
    with app.app_context():
        db.create_all()

    return app

def commit():
    with AppClass.app.app_context():
        db.session.commit()