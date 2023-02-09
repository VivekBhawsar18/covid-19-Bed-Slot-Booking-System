from flask import Flask
from config import Config 
from config import MailConfig 
from Flaskapp.extensions import db , mail , login_manager
from Flaskapp.models.hospital import *
from Flaskapp.models.users import *


app = Flask(__name__)

# App configuration
app.config.from_object(Config)
app.config.from_object(MailConfig)

# Initialize Flask extensions here
db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'home.index'
login_manager.login_message_category = "info"

@login_manager.user_loader
def user_load(user_id):
        user = User.query.get(int(user_id))
        if user:
                return user
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Hospitaluser.query.get(int(user_id))

# Register blueprints here
from Flaskapp.blueprints.home.views import bp as Home_bp
app.register_blueprint(Home_bp)

from Flaskapp.blueprints.test.views import bp as Test_bp
app.register_blueprint(Test_bp ,url_prefix ='/test')

from Flaskapp.blueprints.admin.views import bp as Admin_bp
app.register_blueprint(Admin_bp , url_prefix = '/admin')

from Flaskapp.blueprints.hospital.views import bp as Hospital_bp
app.register_blueprint(Hospital_bp , url_prefix = '/hospital')

from Flaskapp.blueprints.user.views import bp as User_bp
app.register_blueprint(User_bp , url_prefix = '/user')

