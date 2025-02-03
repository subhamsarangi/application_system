from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from routes import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
