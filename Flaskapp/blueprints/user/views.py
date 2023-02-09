'''This code imports the necessary libraries and creates a blueprint for the user functionality.'''
from flask import Blueprint, flash , render_template , request , redirect, session , url_for
from flask_mail import Message
from Flaskapp.extensions import db , mail
from Flaskapp.models.users import *
from Flaskapp.models.hospital import *
from config import AdminCred
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user , login_required, logout_user , current_user


# Creating a blueprint object 'bp' to store the user related functionality
bp = Blueprint('user' , __name__ , static_folder='static' , template_folder='templates')

# Importing the admin credentials from the config file
var = AdminCred()

"""Class for handling OTP generation and updates."""
class otp:
    def __init__(self, otp=000000):
        """Initialize the object with the given OTP value."""
        self.otp = otp

    def update_otp(self, new_otp):
        """Method to update the OTP value."""
        self.otp = new_otp
        return self.otp

# Creating an object of the otp class
obj = otp()

# This code defines a Flask route that handles user login. The route handles both GET and POST requests.
#  [User Login ]
@bp.route('/login', methods=['GET' , 'POST'])
def user_login():

    # If the request method is POST, retrieve the email and password from the form data
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the User table for a user with the given email
        user = User.query.filter_by(email=email).first()

        # If a user with the given email exists
        if user:

            # Check if the provided password matches the hashed password in the database
            password = check_password_hash(user.password , password)
            new_otp = randint(100000,999999)

            # If the password matches, generate a new OTP and send it to the user's email
            if password :

                    obj.update_otp(new_otp)
                    
                    msg = Message(
                            f'Your Email OTP to Login on MediLab is {new_otp}',
                            sender = var.MAIL_SENDER,
                            recipients = [email]
                            )

                    msg.html = render_template('email/loginOtp.html' , name=user.name , sentotp=new_otp)

                    # sending OTP to user's email using flask mail module
                    mail.send(msg)

                    session['email'] = email

                    flash("OTP Sent" ,"success")
                    return render_template("verify/loginVerification.html")
            
            # If the password doesn't match, show an error message
            flash("Incorrect Password" ,"danger")
            return redirect(url_for('user.user_login'))
        
        # If no user with the given email exists, show an error message
        flash('Email not registered . SignUp First.', "danger")
        return redirect(url_for('user.user_signup'))

    # If the request method is GET, return the login template
    return render_template('userLogin.html')


# [ User SignUp ]
@bp.route('/signup', methods=['GET' , 'POST'])
def user_signup():
    """
    This function handles the user sign up process.
    If the request method is POST, it extracts the user input data from the request form, such as name, email, contact, gender, and address.
    It then checks if the entered email or contact is already registered in the database by querying the User model.
    If the email or contact is already registered, it sends a flash message to the user to indicate this.
    If the email and contact are not registered, it generates a new OTP and sends it to the user via email.
    The user's input data is then saved to the session.
    If the request method is GET, it returns the userSignup.html template.
    """

    if request.method=='POST':

        # Extract the user input data from the request form
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        gender = request.form.get('gender')
        address = request.form.get('address')

        # Convert the name to upper case
        name = name.upper()

        # Check if the email or contact is already registered in the database
        userEmail= User.query.filter_by(email=email).first()
        userContact= User.query.filter_by(contact=contact).first()

        # If the email is already registered, send a flash message to the user
        if  userEmail:
            flash("Email is already registered","warning")
            return redirect(url_for('user.user_signup'))
        
        # If the contact is already registered, send a flash message to the user
        if userContact:
            flash("Contact No. is already registered","warning")
            return redirect(url_for('user.user_signup'))           

        # Generate a new OTP and send it to the user via email
        new_otp = randint(000000,999999)
        obj.update_otp(new_otp)


        msg = Message(
                        f'Verify your email {new_otp}',
                        sender = var.MAIL_SENDER,
                        recipients = [email]
                        )

        msg.html = render_template('email/signupOtp.html' , name=name , sentotp=new_otp)

        mail.send(msg)

        # Save the user input data to the session
        session['name']=name
        session['contact']=contact
        session['email']=email
        session['gender']=gender
        session['address']=address

        # Send a flash message to the user to indicate that the OTP has been sent
        flash("OTP sent" , "success")
        return render_template('verify/signupVerification.html')

    # If the request method is GET, return the userSignup.html template
    return render_template('userSignup.html')


# [ Email verification for new user sign up ]
@bp.route('/addUser' , methods=['GET' , 'POST'])
def verify_email():
    
    """
    If user's email OTP matches the generated OTP, the user account will be created and the user will be redirected to the login page.
    """

    if request.method=='POST':

        # Retrieve the data stored in session variables
        name=session['name']
        contact=session['contact']
        email=session['email']
        gender=session['gender']
        address=session['address']

        # Get the OTP entered by the user
        userotp = request.form.get('otp')
        password = request.form.get('password')

        # Hash the password entered by the user
        encpassword = generate_password_hash(password , method='sha256')


        # Check if the OTP entered by the user matches the generated OTP
        if int(userotp) == obj.otp :

            try:
                # Create a new user object
                newuser = User( email=email	,name=name ,contact=contact ,gender=gender , address=address, password=encpassword)
                # Add the user to the database
                db.session.add(newuser)
                # Commit the changes to the database
                db.session.commit()
            except Exception as e :
                # Return error message if there's an error in the database
                return str(e)

            # Send a confirmation email to the user
            msg = Message(
                    f'Congratulations {name}, your account on Medilab has been successfully created.',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

            msg.html = render_template('email/congratulations.html'  , name=name ,email=email , password=password)

            mail.send(msg)

            # Remove the data stored in session variables
            [session.pop(key) for key in list(session.keys())]

            # Display a success message and redirect to the login page
            flash('Congratulations, your account has been successfully created.' , "success")
            return redirect(url_for('user.user_login'))

    # Display an error message if the OTP entered by the user does not match the generated OTP
    flash("wrong OTP..!   try again." , "danger")
    return render_template('verify/signupVerification.html')


# [ User login verification ]
@bp.route('/loginverify', methods=['GET' , 'POST'])
def user_home():

    # Check if the request method is a POST request
    if request.method == 'POST':

        # Retrieve the email from the session
        email = session['email']

        # Query the User object with the email
        user = User.query.filter_by(email=email).first()

        # Get the OTP from the form data
        userotp = request.form.get('otp')

        # Check if the OTP entered by the user matches the OTP stored in the obj object
        if int(userotp) == obj.otp :
            # Log in the user
            login_user(user , remember=False)
            # Redirect the user to the dashboard
            return redirect(url_for('user.user_dashboard'))
        
        # If the OTP entered by the user is incorrect
        flash("wrong OTP..!   try again." , "danger")
        # Render the verification template again
        return render_template('verify/loginVerification.html')
    
    # if the request method is a GET redirect user to login page
    flash('Login first' , 'warning')
    return redirect(url_for('user.user_login'))


# [ User dashboard route ]
@bp.route('/dashboard')
@login_required
def user_dashboard():

    '''This route is used to render the user dashboard page
    The '@login_required' decorator ensures that the user is logged in before accessing this page.
    If the user is not logged in, they will be redirected to the login page.'''

    return render_template('userDashboard.html')


# The code is for a bed slot booking system for a hospital. The function `bed_slot` handles both GET and POST requests. The GET request returns the `bedSlotbooking.html` template, which is a form for booking a bed slot. The POST request processes the form data, checks if the email or phone number of the patient has already been used to book a slot, checks if the entered hospital code is valid, updates the number of available beds of the selected type, adds the booking information to the database, sends a confirmation email to the patient, and finally returns a redirect to the bed slot booking page.

# The function starts by fetching all records from the `hospitaldata` table using the `db.engine.execute` method and storing it in the `query` variable.

# This line defines a route for the URL '/slotbooking' and specifies that it can handle both GET and POST requests.
@bp.route('/slotbooking', methods=['GET' , 'POST'])
# This line specifies that the user must be logged in to access this route.
@login_required
def bed_slot():
    
    # This line fetches all records from the 'hospitaldata' table and stores it in the 'query' variable.
    query = db.engine.execute('SELECT * FROM hospitaldata')

    # If the request method is POST, the form data is processed.
    if request.method=="POST":
        
        # The form data is retrieved and stored in variables.
        email=request.form.get('email')
        hcode=request.form.get('hcode')
        bedtype=request.form.get('bedtype')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        
        # These lines check if the email or phone number has already been used to book a slot
        checkbooking=Userbookings.query.filter_by(email=email).first()
        checkContact = Userbookings.query.filter_by(pphone=pphone).first()

        # If the email has already been used, a warning message is displayed and the user is redirected to the bed slot booking page.
        if checkbooking:
            flash(" Booking exists ","warning")
            return redirect(url_for('user.bed_slot'))
        
        # If the phone number has already been used, a warning message is displayed and the user is redirected to the bed slot booking page.
        if checkContact:
            flash(" Contact No. exists ","warning")
            return redirect(url_for('user.bed_slot'))           
        
        # The hospital code is stored in the 'code' variable.
        code=hcode

        # The data for the hospital with the specified code is fetched from the 'hospitaldata' table.
        dbb=db.engine.execute(f"SELECT * FROM `hospitaldata` WHERE `hospitaldata`.`hcode`='{code}' ")         
        bedtype=bedtype

        # The bed type and the number of available beds (seat) are stored in variables.
        seat = 0

        # Decrement the number of available beds of the selected type in the hospital with the given code
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
        
        # If there is at least one bed of the selected type available in the hospital, book the slot
        if seat>=1:

            # Check if there is a hospital with the given hcode
            check=Hospitaldata.query.filter_by(hcode=hcode).first()

            # If there is a hospital with the given hcode
            if check!=None:
                    try:
                        # Create a new entry in the Userbookings table with the given data
                        res=Userbookings(email=email,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone)
                        db.session.add(res)

                        # Commit the changes to the database
                        db.session.commit()

                    except Exception as e :
                        # Return the error message if any exception occurs
                        return str(e)
                    
                    # Get the hospital details from the Hospitaldata table
                    hospital = Hospitaldata.query.filter_by(hcode=hcode).first()

                    # Create a message object to send an email to the user
                    msg = Message(
                        f'Dear {pname} your booking on Medilab is confirmed!',
                        sender = var.MAIL_SENDER,
                        recipients = [email]
                        )

                    # Set the HTML template for the email
                    msg.html = render_template('email/bookingsuccesfull.html'  , name=pname ,hospital=hospital.hname , bedtype=bedtype , hospitalcode = hospital.hcode)

                    # Send the email
                    mail.send(msg)
                    
                    # Display a success message
                    flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                    # Redirect to the bed_slot page
                    return redirect(url_for('user.bed_slot'))
            else:
                    # Display an error message if the hcode is not valid
                    flash("Give the proper hospital Code","info")
                    # Redirect to the bed_slot page
                    return redirect(url_for('user.bed_slot'))
            
        # Display a warning message if the bedtype is not available in the given hospital
        flash(f'{bedtype} is not available in {d.hname}' , 'warning')
        # Redirect to the bed_slot page
        return redirect(url_for('user.bed_slot'))
    
    # Render the services/bedSlotbooking.html template with the list of hospitals
    return render_template('services/bedSlotbooking.html', query=list(query))


# [ This router will render user booking page ]
@bp.route("/myBooking",methods=['GET' , 'POST'])
@login_required
def user_booking():

    # initialize the hospital name
    hospital = ''

    # get the email of the current user
    email=current_user.email

    # retrieve the user booking data based on the email
    data=Userbookings.query.filter_by(email=email).first()

    # if the user has made a booking
    if data:
        # get the hospital code
        hcode = data.hcode

        # get the hospital name based on the hospital code
        hospitalname = Hospitaldata.query.filter_by(hcode=hcode).first()
        hospital = hospitalname.hname
        session['hospital'] = hospital
    pass

    # if the request method is POST
    if request.method == 'POST':

        # get the form data
        name = request.form.get('name')
        contact =  request.form.get('contact')
        oxygen = request.form.get('oxygen')
        name = name.upper()

        # get the user booking data based on the email
        userContact = Userbookings.query.filter_by(email=email).first()
        # check if the contact number is already registered
        allContact = Userbookings.query.filter_by(pphone=contact).first()

        # if the contact number is already registered
        if allContact:
            # if the contact number is already registered for the same user
            if userContact.pphone == contact:
                # update the user booking data
                data.pname = name
                data.pphone = contact
                data.spo2 = oxygen

                # commit the changes to the database
                db.session.commit()

                # show a success message
                flash('Booking details updated successfully.' , 'primary')
                # redirect the user to the booking page
                return redirect(url_for('user.user_booking'))
            
            # if the contact number is registered for a different user
            flash('Contact No. is already registered' , 'warning')
            # render the update booking template with the data and hospital name
            return render_template("services/updateBooking.html",data=data , hospital=hospital)
        
        # update the user booking data
        data.pname = name
        data.pphone = contact
        data.spo2 = oxygen

        # commit the changes to the database
        db.session.commit()

        # show a success message
        flash('Booking details updated successfully.' , 'primary')
        # redirect the user to the booking page
        return redirect(url_for('user.user_booking'))

    # render the booking template with the data and hospital name
    return render_template("services/booking.html",data=data , hospital=hospital)


# [ Update booking route ]
@bp.route("/updateBooking")
@login_required
def update_booking():

    # Get the current user's email
    email = current_user.email

    # Get the name of the hospital that the user has booked a slot in
    hospital = session['hospital']

    # Get the user's booking information based on their email
    data = Userbookings.query.filter_by(email=email).first()

    # Show a success message that the user can now update their booking details
    flash('You can now update your booking details.' , 'success')
    # Render the template for updating booking details with the user's booking information and the name of the hospital
    return render_template("services/updateBooking.html",data=data , hospital=hospital)


# [ Delete booking route ]
@bp.route('/delete')
@login_required
def user_booking_delete():

    # Get the current user email
    email = current_user.email

    # Get the Userbookings data based on email
    data = Userbookings.query.filter_by(email=email).first()

    # Get the hcode and bedtype from the Userbookings data
    hcode = data.hcode
    bedtype = data.bedtype

    # Get the hospital data based on the hcode
    hospital = Hospitaldata.query.filter_by(hcode=hcode).first()
    seat = 0

    # Increment the number of available beds in the hospital based on the bedtype
    if bedtype=='NormalBed':
        seat = hospital.normalbed
        hospital.normalbed = seat+1

    if bedtype=='HICUBed':
        seat = hospital.hicubed
        hospital.hicubed = seat+1

    if bedtype=='ICUBed':
        seat = hospital.icubed
        hospital.icubed = seat+1

    if bedtype=='VENTILATORBed':
        seat = hospital.vbed
        hospital.vbed = seat+1
    else :
        pass
    
    # Commit the changes to the database
    db.session.commit()

    # Delete the Userbookings data based on the email
    Userbookings.query.filter_by(email=email).delete()
    # Commit the changes to the database
    db.session.commit()
    flash("Data Deleted Succesfully" , "danger")

    return redirect(url_for('user.user_booking'))


# [ User account page ]
@bp.route("/account",methods=['GET' , 'POST'])
@login_required
def user_account():

    # Get the current user email
    email = current_user.email
    # Query the user data based on the email
    data = User.query.filter_by(email=email).first()    

    if request.method == 'POST':

        # Get the form data
        name = request.form.get('name')
        contact = request.form.get('contact')
        address = request.form.get('address')
        # Convert name to uppercase
        name = name.upper()

        # Query user data based on the email
        userContact = User.query.filter_by(email=email).first()
        # Query to check if the contact already exists in the database
        allContact = User.query.filter_by(contact=contact).first()

        # Check if the contact already exists
        if allContact:
            # Check if the contact belongs to the current user
            if userContact.contact == contact:
                # Update the user details
                data.name = name
                data.contact = contact
                data.address = address

                db.session.commit()

                flash('Account details updated successfully.' , 'primary')
                return render_template("services/account.html",data=data)

            flash('Contact No. is already registered' , 'warning')
            return render_template("services/updateAccount.html",data=data)
        
        # Update the user details if the contact does not already exists
        data.name = name
        data.contact = contact
        data.address = address

        db.session.commit()

        flash('Account details updated successfully.' , 'primary')
        return render_template("services/account.html",data=data)

    return render_template("services/account.html",data=data)


# [ User update account page ]
@bp.route("/updateAccount")
@login_required
def account_update():

    # Get the email of the current logged in user
    email = current_user.email
    # Get the user data from the database using email
    data = User.query.filter_by(email=email).first()

    # Show a success flash message
    flash('You can now update your account details.' , 'success')
    # Render the template for update account page and pass the user data
    return render_template("services/updateAccount.html",data=data)


# [ Logout Route for a user]
@bp.route('/logout', methods=['GET' , 'POST'])
@login_required
def user_logout():
    # logout the user using the logout_user function from Flask-Login
    logout_user()
    # Display a success message
    flash('Logout Successfull' , 'success')
    # Redirect the user to the login page
    return redirect(url_for('user.user_login'))



