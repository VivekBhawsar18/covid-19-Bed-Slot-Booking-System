from flask import Blueprint, flash , render_template , request , redirect , url_for
from Flaskapp.models.hospital import *
from Flaskapp.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , login_required, logout_user , current_user

bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )

@bp.route('/login')
def hospital_login():
    return render_template('hlogin.html')


@bp.route('/login' , methods=['POST'])
def hospital_home():
        # login code goes here
        email=request.form.get('email')
        password=request.form.get('password')

        user=Hospitaluser.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not  check_password_hash(user.password,password):

            flash('Please check your login details and try again.' ,'danger')
            return redirect(url_for('hospital.hospital_login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for('hospital.hospital_dashboard' , name=current_user.email))

@bp.route('/dashboard')
@login_required
def hospital_dashboard():
    return render_template('hdashboard.html')

@bp.route('/add/info')
def hospital_info():
    pass

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logout ", "primary")
    return redirect(url_for('hospital.hospital_login'))