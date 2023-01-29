from flask import Blueprint , render_template , request , redirect , url_for
import os

bp = Blueprint('admin' , __name__ , static_folder='static' , template_folder='templates')

@bp.route('/login')
def admin_login():
    return render_template('alogin.html')

@bp.route('/home' , methods=['POST' , 'GET'])
def home():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        name = os.environ.get('ADMIN_NAME')
        pwd  = os.environ.get('ADMIN_PASS')

        if ( username==name and password==pwd ):
            return "<h1>Login success</h1>"

        else:
            return "<h1>Login failed</h1>"
    return redirect(url_for('login'))

