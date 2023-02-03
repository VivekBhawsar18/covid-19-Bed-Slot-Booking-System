from flask import Blueprint, flash , render_template , request , redirect , url_for , session
from Flaskapp.extensions import db , mail
from Flaskapp.models.hospital import *
from config import AdminCred
from flask_mail import Message
from werkzeug.security import generate_password_hash

bp = Blueprint('admin' , __name__ , static_folder='static' , template_folder='templates')

var = AdminCred()

# admin login
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


# adding new hospital user 
@bp.route("/add", methods=['POST' , 'GET'])
def hos_user():

        # Checking in session if admin is present or not 
        if request.method=='POST' and session['user']==var.ADMIN_NAME:

            # Data to be saved in db .
            hcode = request.form.get('hcode')
            email = request.form.get('email')
            password = request.form.get('password')

            # Encrypting user-supplied password before saving it into db .
            encpassword = generate_password_hash(password , method='sha256')
            hcode=hcode.upper() 
            
            userEmail= Hospitaluser.query.filter_by(email=email).first()
            userHcode = Hospitaluser.query.filter_by(hcode=hcode).first() 


            # this is method to check if the user-supplied email already exists .
            if  userEmail:
                flash("Email is already taken","warning")
                return render_template('adminHome.html')

            # this is method to check check if the user-supplied Hospital Code already exists .
            elif userHcode :
                flash("Hcode is already taken","warning")
                return render_template('adminHome.html')       
                

            # if the above check passes, then we know the user-supplied data is unique.
            # this is method  to send email.
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


# admin logout 
@bp.route("/logout")
def admin_logout():
    
    session.pop('user')
    flash("You are logout admin", "primary")

    return redirect(url_for('admin.admin_login'))