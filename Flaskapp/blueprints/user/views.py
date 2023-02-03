from flask import Blueprint, flash , render_template , request , redirect, session , url_for
from flask_mail import Message
from Flaskapp.extensions import db , mail
from Flaskapp.models.users import *
from config import AdminCred
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user' , __name__ , static_folder='static' , template_folder='templates')

var = AdminCred()

class otp:

    otp = 0000
    
    def new_otp(self , otp):
        self.otp = otp
        return otp

obj = otp()

@bp.route('/login', methods=['GET' , 'POST'])
def user_login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:

            password = check_password_hash(user.password , password)

            if password:
                new_otp = randint(0000,9999)
                obj.new_otp(new_otp)

                msg = Message(
                    f'Your Email OTP to Login on MediLab is {new_otp}',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

                msg.html = render_template('loginOtp.html' , name=user.firstname , sentotp=new_otp)

                mail.send(msg)

                flash("OTP Sent" ,"success")
                return render_template("loginVerification.html")

            flash("Incorrect Password" ,"danger")
            return redirect(url_for('user.user_login'))

        flash('Email not registered . SignUp First.', "danger")
        return redirect(url_for('user.user_login'))


    return render_template('userLogin.html')


@bp.route('/signup', methods=['GET' , 'POST'])
def user_signup():

    if request.method=='POST':

        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        dob = request.form.get('dob')

        first_name = first_name.upper()
        last_name = last_name.upper()

        userEmail= User.query.filter_by(email=email).first()

        # if  userEmail :

        if  userEmail:
            flash("Email is already taken","warning")
            return redirect(url_for('user.user_signup'))

        new_otp = randint(0000,9999)
        obj.new_otp(new_otp)

        msg = Message(
                    f'Your Email OTP to Signup on MediLab is {new_otp}',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

        msg.html = render_template('otp.html' , name=first_name , sentotp=new_otp)

        mail.send(msg)

        session['firstname']=first_name
        session['lastname']=last_name
        session['email']=email
        session['dob']=dob


        flash("OTP sent" , "success")
        return render_template('emailVerification.html')
        
    return render_template('userSignup.html')

# @bp.context_processor
# def context_processor():
#     return dict(sentotp=otp)

@bp.route('/addUser' , methods=['GET' , 'POST'])
def verify_email():

    if request.method=='POST':

        first_name=session['firstname']
        last_name=session['lastname']
        email=session['email']
        dob=session['dob']

        userotp = request.form.get('otp')
        password = request.form.get('password')


        encpassword = generate_password_hash(password , method='sha256')

        if int(userotp) == obj.otp :
            newuser = User( email=email	,firstname=first_name ,lastname=last_name ,dob=dob ,password=encpassword)
            db.session.add(newuser)
            db.session.commit()

            msg = Message(
                    f'Congratulations {first_name}, your account on Medilab has been successfully created.',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

            msg.html = render_template('succes.html'  , name=first_name ,email=email , password=password)

            mail.send(msg)

            flash('Congratulations, your account has been successfully created.' , "success")
            return redirect(url_for('user.user_login'))

    
    flash("wrong OTP..!   try again." , "danger")
    return render_template('emailVerification.html')


@bp.route('/home', methods=['GET' , 'POST'])
def user_home():
    if request.method == 'POST':

        userotp = request.form.get('otp')

        if int(userotp) == obj.otp :
            return "<h1>Correct OTP</h1>"
        flash("wrong OTP..!   try again." , "danger")
        return render_template('loginVerification.html')