from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
session = Session()