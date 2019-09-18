"""Sandman2 main application setup code."""

# Third-party imports
from flask import Flask, current_app, jsonify

# Application imports
from flask_sandman.database import DATABASE as db
from flask_sandman.api import sandman
from flask_admin import Admin
from flask_httpauth import HTTPBasicAuth

# Augment flask_sandman's Model class with the Automap and Flask-SQLAlchemy model
# classes
auth = HTTPBasicAuth()

def get_app(
        database_uri,
        exclude_tables=None,
        user_models=None,
        reflect_all=True,
        read_only=False,
        schema=None):
    """Return an application instance connected to the database described in
    *database_uri*.

    :param str database_uri: The URI connection string for the database
    :param list exclude_tables: A list of tables to exclude from the API
                                service
    :param list user_models: A list of user-defined models to include in the
                             API service
    :param bool reflect_all: Include all database tables in the API service
    :param bool read_only: Only allow HTTP GET commands for all endpoints
    :param str schema: Use the specified named schema instead of the default
    """
    app = Flask('flask_sandman')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SANDMAN2_READ_ONLY'] = read_only
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.classes = []
    db.init_app(app)
    admin = Admin(app, base_template='layout.html', template_mode='bootstrap3')
    sandman(app,db,user_models or [], exclude_tables or [], admin, read_only, schema)
    return app



