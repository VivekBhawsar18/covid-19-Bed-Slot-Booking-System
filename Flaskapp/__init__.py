from flask import Flask
from config import Config
from Flaskapp.extensions import db

app = Flask(__name__)

# App configuration
app.config.from_object(Config)

# Initialize Flask extensions here
db.init_app(app)

@app.route('/')
def index():
    return "<h1>Home</h1>"

# Register blueprints here
from Flaskapp.test.views import bp as Test_bp
app.register_blueprint(Test_bp ,url_prefix ='/test')

from Flaskapp.home.views import bp as Home_bp
app.register_blueprint(Home_bp , url_prefix = '/home')

from Flaskapp.admin.views import bp as Admin_bp
app.register_blueprint(Admin_bp , url_prefix = '/admin')