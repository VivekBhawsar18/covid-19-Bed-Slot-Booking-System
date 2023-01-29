from flask import Blueprint , render_template , request , redirect , url_for

bp = Blueprint('user' , __name__ , static_folder='static' , template_folder='templates')

@bp.route('/login')
def user_login():
    return render_template('userLogin.html')

@bp.route('/signup')
def user_signup():
    return render_template('userSignup.html')