from flask import Blueprint, flash , render_template , request , redirect , url_for , session
import os
from flask_bcrypt import Bcrypt


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

        else:
            flash("Invalid Credentials","danger")
            return redirect(url_for('admin.admin_login'))

    return redirect(url_for('admin.admin_login'))

@bp.route("/add/user", methods=['POST' , 'GET'])
def hos_user():

        if request.method=='POST':
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')

            encpassword=Bcrypt.generate_password_hash(password)
            hcode=hcode.upper() 
            
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            hcodeUser = Hospitaluser.query.filter_by(hcode=hcode).first()

            # if  emailUser or hcodeuser:
            if  emailUser:
                flash("Email is already taken","warning")
                return render_template("addHosUser.html")

            elif hcodeUser :
                flash("Hcode is already taken","warning")
                return render_template("addHosUser.html")       

            # this is method  to save data in db
            newhuser=Hospitaluser(hcode=hcode,email=email,password=encpassword)
            db.session.add(newhuser)
            db.session.commit()

        else:
            flash("Login and try Again","warning")
            return render_template("addHosUser.html")

@bp.route("/logout")
def admin_logout():
    
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect(url_for('admin.admin_login'))