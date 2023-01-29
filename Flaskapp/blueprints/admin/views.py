from flask import Blueprint, flash , render_template , request , redirect , url_for , session
import os

bp = Blueprint('admin' , __name__ , static_folder='static' , template_folder='templates')

@bp.route('/login')
def admin_login():
    return render_template('adminLogin.html')

@bp.route('/home' , methods=['POST' , 'GET'])
def admin_home():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        name = os.environ.get('ADMIN_NAME')
        pwd  = os.environ.get('ADMIN_PASS')

        if ( username==name and password==pwd ):
            session['user'] = name
            flash("login success","info")
            return render_template('adminHome.html')
            return "Login succes"

        else:
            flash("Invalid Credentials","danger")
            return redirect(url_for('admin.admin_login'))
            return "Login failed"

    return redirect(url_for('admin.admin_login'))

@bp.route("/logoutAdmin")
def admin_logout():
    
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect(url_for('admin.admin_login'))