import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    from app import routes, models  # make sure routes/models use `current_app` if needed
    return app
