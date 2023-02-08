from flask import Blueprint, flash , render_template , request , redirect, session , url_for
from flask_mail import Message
from Flaskapp.extensions import db , mail , login_manager
from Flaskapp.models.users import *
from Flaskapp.models.hospital import *
from config import AdminCred
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user , login_required, logout_user , current_user

bp = Blueprint('user' , __name__ , static_folder='static' , template_folder='templates')


var = AdminCred()

class otp:

    otp = 000000
    
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
            new_otp = randint(100000,999999)

            if password :

                    obj.new_otp(new_otp)
                    
                    msg = Message(
                            f'Your Email OTP to Login on MediLab is {new_otp}',
                            sender = var.MAIL_SENDER,
                            recipients = [email]
                            )

                    msg.html = render_template('email/loginOtp.html' , name=user.name , sentotp=new_otp)

                    mail.send(msg)

                    session['email'] = email

                    flash("OTP Sent" ,"success")
                    return render_template("verify/loginVerification.html")
                
            flash("Incorrect Password" ,"danger")
            return redirect(url_for('user.user_login'))

        flash('Email not registered . SignUp First.', "danger")
        return redirect(url_for('user.user_signup'))


    return render_template('userLogin.html')


@bp.route('/signup', methods=['GET' , 'POST'])
def user_signup():

    if request.method=='POST':

        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        gender = request.form.get('gender')
        address = request.form.get('address')

        name = name.upper()

        userEmail= User.query.filter_by(email=email).first()
        userContact= User.query.filter_by(contact=contact).first()


        if  userEmail:
            flash("Email is already registered","warning")
            return redirect(url_for('user.user_signup'))
        
        if userContact:
            flash("Contact No. is already registered","warning")
            return redirect(url_for('user.user_signup'))           

        new_otp = randint(000000,999999)
        obj.new_otp(new_otp)


        msg = Message(
                        f'Verify your email {new_otp}',
                        sender = var.MAIL_SENDER,
                        recipients = [email]
                        )

        msg.html = render_template('email/signupOtp.html' , name=name , sentotp=new_otp)

        mail.send(msg)

        session['name']=name
        session['contact']=contact
        session['email']=email
        session['gender']=gender
        session['address']=address


        flash("OTP sent" , "success")
        return render_template('verify/signupVerification.html')
        
        
    return render_template('userSignup.html')


@bp.route('/addUser' , methods=['GET' , 'POST'])
def verify_email():

    if request.method=='POST':

        name=session['name']
        contact=session['contact']
        email=session['email']
        gender=session['gender']
        address=session['address']

        userotp = request.form.get('otp')
        password = request.form.get('password')


        encpassword = generate_password_hash(password , method='sha256')

        if int(userotp) == obj.otp :

            try:
                newuser = User( email=email	,name=name ,contact=contact ,gender=gender , address=address, password=encpassword)
                db.session.add(newuser)
                db.session.commit()
            except Exception as e :
                return str(e)

            msg = Message(
                    f'Congratulations {name}, your account on Medilab has been successfully created.',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

            msg.html = render_template('email/congratulations.html'  , name=name ,email=email , password=password)

            mail.send(msg)

            [session.pop(key) for key in list(session.keys())]
            flash('Congratulations, your account has been successfully created.' , "success")
            return redirect(url_for('user.user_login'))

    
    flash("wrong OTP..!   try again." , "danger")
    return render_template('verify/signupVerification.html')


@bp.route('/loginverify', methods=['GET' , 'POST'])
def user_home():
    if request.method == 'POST':

        email = session['email']
        print(email)

        user = User.query.filter_by(email=email).first()
        userotp = request.form.get('otp')

        if int(userotp) == obj.otp :

            login_user(user , remember=False)
            return redirect(url_for('user.user_dashboard'))
        
        flash("wrong OTP..!   try again." , "danger")
        return render_template('verify/loginVerification.html')


@bp.route('/dashboard', methods=['GET' , 'POST'])
@login_required
def user_dashboard():
    return render_template('userDashboard.html')


@bp.route('/slotbooking', methods=['GET' , 'POST'])
@login_required
def bed_slot():
    
    query = db.engine.execute('SELECT * FROM hospitaldata')

    if request.method=="POST":
        
        email=request.form.get('email')
        hcode=request.form.get('hcode')
        bedtype=request.form.get('bedtype')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        
        checkbooking=Userbookings.query.filter_by(email=email).first()
        checkContact = Userbookings.query.filter_by(pphone=pphone).first()

        if checkbooking:
            flash(" Booking exists ","warning")
            return redirect(url_for('user.bed_slot'))
        if checkContact:
            flash(" Contact No. exists ","warning")
            return redirect(url_for('user.bed_slot'))           
        
        code=hcode
        dbb=db.engine.execute(f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`hcode`='{code}' ")         
        bedtype=bedtype
        seat = 0

        if bedtype=="NormalBed":
            for d in dbb:
                seat=d.normalbed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.normalbed=seat-1

                
        elif bedtype=="HICUBed":      
            for d in dbb:
                seat=d.hicubed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.hicubed=seat-1


        elif bedtype=="ICUBed":     
            for d in dbb:
                seat=d.icubed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.icubed=seat-1

        elif bedtype=="VENTILATORBed": 
            for d in dbb:
                seat=d.vbed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.vbed=seat-1

        else:
            pass
        
        if seat>=1:

            check=Hospitaldata.query.filter_by(hcode=hcode).first()
            if check!=None:
                    try:
                        res=Userbookings(email=email,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone)
                        db.session.add(res)
                        db.session.commit()
                    except Exception as e :
                        return str(e)
                    
                    hospital = Hospitaldata.query.filter_by(hcode=hcode).first()

                    msg = Message(
                        f'Dear {pname} your booking on Medilab is confirmed!',
                        sender = var.MAIL_SENDER,
                        recipients = [email]
                        )

                    msg.html = render_template('email/bookingsuccesfull.html'  , name=pname ,hospital=hospital.hname , bedtype=bedtype , hospitalcode = hospital.hcode)

                    mail.send(msg)
                    
                    flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                    return redirect(url_for('user.bed_slot'))
            else:
                    flash("Give the proper hospital Code","info")
                    return redirect(url_for('user.bed_slot'))
            
        flash(f'{bedtype} is not available in {d.hname}' , 'warning')
        return redirect(url_for('user.bed_slot'))               

    return render_template('services/bedSlotbooking.html', query=list(query))


@bp.route("/myBooking",methods=['GET' , 'POST'])
@login_required
def user_booking():
    hospital = ''
    email=current_user.email
    data=Userbookings.query.filter_by(email=email).first()
    if data:
        hcode = data.hcode
        hospitalname = Hospitaldata.query.filter_by(hcode=hcode).first()
        hospital = hospitalname.hname
        session['hospital'] = hospital
    pass


    if request.method == 'POST':

        name = request.form.get('name')
        contact =  request.form.get('contact')
        oxygen = request.form.get('oxygen')
        name = name.upper()

        userContact = Userbookings.query.filter_by(email=email).first()
        allContact = Userbookings.query.filter_by(pphone=contact).first()

        if allContact:

            if userContact.pphone == contact:

                data.pname = name
                data.pphone = contact
                data.spo2 = oxygen

                db.session.commit()

                flash('Booking details updated successfully.' , 'primary')
                return redirect(url_for('user.user_booking'))

            flash('Contact No. is already registered' , 'warning')
            return render_template("services/updateBooking.html",data=data , hospital=hospital)
        
        data.pname = name
        data.pphone = contact
        data.spo2 = oxygen

        db.session.commit()

        flash('Booking details updated successfully.' , 'primary')
        return redirect(url_for('user.user_booking'))


    return render_template("services/booking.html",data=data , hospital=hospital)


@bp.route("/updateBooking")
@login_required
def update_booking():

    email = current_user.email
    hospital = session['hospital']
    data = Userbookings.query.filter_by(email=email).first()

    flash('You can now update your booking details.' , 'success')
    return render_template("services/updateBooking.html",data=data , hospital=hospital)

@bp.route('/delete')
@login_required
def user_booking_delete():
    email = current_user.email

    Userbookings.query.filter_by(email=email).delete() # Taking current_user id and delete its all data stored in database
    db.session.commit()
    flash("Data Deleted Succesfully" , "danger")

    return redirect(url_for('user.user_booking'))


@bp.route("/account",methods=['GET' , 'POST'])
@login_required
def user_account():

    email = current_user.email
    data = User.query.filter_by(email=email).first()    

    if request.method == 'POST':

        name = request.form.get('name')
        contact = request.form.get('contact')
        address = request.form.get('address')
        name = name.upper()

        userContact = User.query.filter_by(email=email).first()
        allContact = User.query.filter_by(contact=contact).first()

        if allContact:

            if userContact.contact == contact:

                data.name = name
                data.contact = contact
                data.address = address

                db.session.commit()

                flash('Account details updated successfully.' , 'primary')
                return render_template("services/account.html",data=data)

            flash('Contact No. is already registered' , 'warning')
            return render_template("services/updateAccount.html",data=data)
        
        data.name = name
        data.contact = contact
        data.address = address

        db.session.commit()

        flash('Account details updated successfully.' , 'primary')
        return render_template("services/account.html",data=data)

    return render_template("services/account.html",data=data)


@bp.route("/updateAccount")
@login_required
def account_update():

    email = current_user.email
    data = User.query.filter_by(email=email).first()

    flash('You can now update your account details.' , 'success')
    return render_template("services/updateAccount.html",data=data)



@bp.route('/logout', methods=['GET' , 'POST'])
@login_required
def user_logout():

    logout_user()
    flash('Logout Successfull' , 'success')
    return redirect(url_for('user.user_login'))



