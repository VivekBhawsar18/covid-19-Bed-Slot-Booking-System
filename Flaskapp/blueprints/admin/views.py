from flask import Blueprint, flash , render_template , request , redirect , url_for , session
from Flaskapp.extensions import db , mail
from Flaskapp.models.hospital import *
from config import AdminCred
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('admin' , __name__ , static_folder='static' , template_folder='templates')

var = AdminCred()


@bp.route('/login' , methods=['POST' , 'GET'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        admin_name = var.ADMIN_NAME
        admin_pwd  = var.ADMIN_PWD
            
        if ( username==admin_name and password==admin_pwd ):
            session['user'] = admin_name
            flash("login success","success")
            return render_template('adminHome.html')

        else:
            flash("Invalid Credentials","danger")
            return redirect(url_for('admin.admin_login'))

    return render_template('adminLogin.html')

@bp.route("/add", methods=['POST' , 'GET'])
def hos_user():

        if request.method=='POST' and session['user']==var.ADMIN_NAME:

            hcode = request.form.get('hcode')
            email = request.form.get('email')
            password = request.form.get('password')

            encpassword = generate_password_hash(password , method='sha256')
            hcode=hcode.upper() 
            
            userEmail= Hospitaluser.query.filter_by(email=email).first()
            userHcode = Hospitaluser.query.filter_by(hcode=hcode).first()

            # if  userEmail or userHcode:
            if  userEmail:
                flash("Email is already taken","warning")
                return render_template('adminHome.html')

            elif userHcode :
                flash("Hcode is already taken","warning")
                return render_template('adminHome.html')       
                

            msg = Message(
                    f' COVID CARE CENTER Congratulation .! You can now Login on MediLab',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

            msg.html = render_template('successEmail.html' , hcode=hcode , email=email , password=password )

            mail.send(msg)

            # this is method  to save data in db
            newuser = Hospitaluser( hcode=hcode, email=email, password=encpassword ) 
            db.session.add(newuser)
            db.session.commit()
            print(var.MAIL_SENDER)

            flash("Mail Sent and Data Inserted Successfully","success")
            return render_template("adminHome.html")

        
        flash("Login and try Again","warning")
        return redirect(url_for('admin.admin_login'))

@bp.route("/logout")
def admin_logout():
    
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect(url_for('admin.admin_login'))