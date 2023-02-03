from flask import Blueprint, render_template

bp = Blueprint('home' , __name__ , static_folder='static' , template_folder='templates')

# Home page of app
@bp.route('/')
def index():
    return render_template('home.html')