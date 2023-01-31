from flask import Blueprint, flash , render_template , request , redirect , url_for
from Flaskapp.models.hospitalUser import *
from Flaskapp.extensions import db , bcrypt 

bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )

@bp.route('/login')
def hospital_login():
    return render_template('hlogin.html')

@bp.route('/home' , methods=['GET' , 'POST'])
def hospital_home():

    if request.method=="POST":
        email=request.form.get('email')
        pwd=request.form.get('password')

        user=Hospitaluser.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password,pwd):
            # login_user(user)
            # flash("Login Success","info")
            # session.pop('srfid', None)
            # session.clear()
            # return render_template("index.html")
            return "<h1>Login success</h1>"
        else:
            # flash("Invalid Credentials","danger")
            # return render_template("hospitallogin.html")
            return "<h1>login fail</h1>"

    return render_template('hospitallogin.html')

