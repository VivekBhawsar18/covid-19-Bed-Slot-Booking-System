# Importing required packages and modules from the Flask library
from flask import Flask 
# Importing custom configuration classes for the application
from config import Config 
from config import MailConfig 
# Importing extensions for the application such as database, email and login management
from Flaskapp.extensions import db , mail , login_manager , session 
# Importing models for the hospital and users
from Flaskapp.models.hospital import *
from Flaskapp.models.users import *

import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn="https://86bdac5970d94915bf25623282ca4592@o4504660581482496.ingest.sentry.io/4504660582924288",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# Creating a Flask application instance
app = Flask(__name__)


# App configuration

# Configuring the application using the custom configuration classes
# The Config class contains the basic configuration details for the application
# The MailConfig class contains the configuration details for the email service
app.config.from_object(Config)
app.config.from_object(MailConfig)
app.config['SESSION_TYPE'] = 'filesystem'



# Initializing extensions for the Flask applicatio

# The database extension is initialized
db.init_app(app)
# The email extension is initialized
mail.init_app(app)
# The login management extension is initialized
login_manager.init_app(app)
# The session management extension is initialized
session.init_app(app)
# Setting the login view for the application
login_manager.login_view = 'home.index'
# Setting the message category for the login messages in the application
login_manager.login_message_category = "info"



# Defining a user_loader function for the login manager extension
# The function takes the user_id as an argument and returns the corresponding user object
@login_manager.user_loader
def user_load(user_id):
        
        # Querying for the user in the Hospitaluser model
        user = Hospitaluser.query.get(int(user_id))
        if user and user.role == 'hospital':
                # If a user is found, return it
                return user
        # If a user is not found in the Hospitaluser model, Querying for the user with the given user_id from the user model
        return User.query.get(int(user_id))


# Registering blueprints for the application

# The home blueprint is registered with the application
from Flaskapp.blueprints.home.views import bp as Home_bp
app.register_blueprint(Home_bp)

# The test blueprint is registered with the application and is prefixed with '/test'
from Flaskapp.blueprints.test.views import bp as Test_bp
app.register_blueprint(Test_bp ,url_prefix ='/test')

# The admin blueprint is registered with the application and is prefixed with '/admin'
from Flaskapp.blueprints.admin.views import bp as Admin_bp
app.register_blueprint(Admin_bp , url_prefix = '/admin')

# The hospital blueprint is registered with the application and is prefixed with '/hospital'
from Flaskapp.blueprints.hospital.views import bp as Hospital_bp
app.register_blueprint(Hospital_bp , url_prefix = '/hospital')

# The user blueprint is registered with the application and is prefixed with '/user'
from Flaskapp.blueprints.user.views import bp as User_bp
app.register_blueprint(User_bp , url_prefix = '/user')

