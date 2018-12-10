import os

try:
    import config
    from flask import Flask
    from bin.routes import routes
    from bin.models import model, db, guard
    from bin.controllers import ErrorController as EC
    import pymysql
    pymysql.install_as_MySQLdb()
    from flask.logging import default_handler
    import logging
except ImportError as IE:
    print(IE)

# Handles http error codes
def http_error(e):
    return EC.error(e), e.code

def create_app(test_config=None):
    """
    Creates and configures the Flask App
    1. Initializes Database Configs
    2. Initializes the Logging file
    3. Initializes Error handlers
    4. Initializes Blueprints
    5. Creates the Database if it doesn't already exist
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.secret_key,
    )
    # Defines database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{config.db_username}:{config.db_password}@localhost/{config.db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.db_track
    app.config['JWT_ACCESS_LIFESPAN'] = config.jwt_access
    app.config['JWT_REFRESH_LIFESPAN'] = config.jwt_refresh

    # Defines the logging file, mode, and format
    logging.basicConfig(filename=config.logging_file, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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
