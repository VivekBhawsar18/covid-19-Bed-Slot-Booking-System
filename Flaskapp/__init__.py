from flask import Flask, session
from config import Config 
from config import MailConfig 
from Flaskapp.extensions import db , bcrypt , mail

app = Flask(__name__)

# App configuration
app.config.from_object(Config)
app.config.from_object(MailConfig)

# Initialize Flask extensions here
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)


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

