'''This code imports the necessary libraries and creates a blueprint for the user functionality.'''
from flask import Blueprint, flash , render_template , request , redirect , url_for , session
from Flaskapp.extensions import db , mail
from Flaskapp.models.hospital import *
from config import AdminCred
from flask_mail import Message
from werkzeug.security import generate_password_hash

# Creating a blueprint object 'bp' to store the user related functionality
bp = Blueprint('admin' , __name__ , static_folder='static' , template_folder='templates')

var = AdminCred()

# [ Admin login functionality ]
@bp.route('/login' , methods=['POST' , 'GET'])
def admin_login():
    # Check the request method
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username') 
        password = request.form.get('password')

        # Get the expected username and password from the constant variables
        admin_name = var.ADMIN_NAME
        admin_pwd  = var.ADMIN_PWD
            
        # Check if the entered username and password match the expected values
        if ( username==admin_name and password==admin_pwd ):
            # Login success, show success message and redirect to the dashboard
            flash("login success","success")
            session['user'] = admin_name
            return redirect(url_for('admin.admin_dashboard'))

        else:
            # Login failed, show error message and redirect back to the login page
            flash("Invalid Credentials","danger")
            return redirect(url_for('admin.admin_login'))
        
    # Return the login template for GET requests
    return render_template('adminLogin.html')


# [ Admin dashboard ]
@bp.route('/dashboard')
def admin_dashboard():
    
    # Check if the user is logged in and the username matches the expected value
    if 'user' in session and session['user']==var.ADMIN_NAME:
        return render_template('adminDashboard.html') # User is logged in, show the dashboard
    # User is not logged in, show error message and redirect to the login page
    flash("Login and try Again","warning")
    return redirect(url_for('admin.admin_login'))


# Services 

# [ Adding new hospital user ]
@bp.route("/add", methods=['POST' , 'GET'])
def hos_user():

        # Check if the request method is POST and the user is logged in with the correct username
        if request.method=='POST'  and 'user' in session and session['user']==var.ADMIN_NAME:
            
            # Get the form data
            hcode = request.form.get('hcode')
            email = request.form.get('email')
            password = request.form.get('password')

            # Hash the password
            encpassword = generate_password_hash(password , method='sha256')
            # Convert the hcode to uppercase
            hcode=hcode.upper() 
            
            # Check if the email or hcode are already taken
            userEmail= Hospitaluser.query.filter_by(email=email).first()
            userHcode = Hospitaluser.query.filter_by(hcode=hcode).first() 

            # If email is already taken, show error message and return to the previous page
            if  userEmail:
                flash("Email is already taken","warning")
                return render_template('services/addHospital.html')

            # If hcode is already taken, show error message and return to the previous page
            elif userHcode :
                flash("Hcode is already taken","warning")
                return render_template('services/addHospital.html')       
                
            # Create and send an email to the new hospital user
            msg = Message(
                    f' COVID CARE CENTER Congratulation .! You can now Login on MediLab',
                    sender = var.MAIL_SENDER,
                    recipients = [email]
                    )

            msg.html = render_template('email/newHospital.html' , hcode=hcode , email=email , password=password )

            mail.send(msg)

            # Add the new hospital user to the database
            try:
                newuser = Hospitaluser( hcode=hcode, email=email, password=encpassword ) 
                db.session.add(newuser)
                db.session.commit()

                # Show success message and redirect to the previous page
                flash("Mail Sent and Data Inserted Successfully","success")
                return redirect(url_for('admin.hos_user'))
            
            except Exception as e :
                # Rollback the transaction if an error occurs
                db.rollback()
                return str(e)

        # Check if the request method is GET and the user is logged in with the correct username
        if request.method=='GET' and 'user' in session and session['user']==var.ADMIN_NAME:
            # Return the add hospital template
            return render_template('services/addHospital.html')
        
        # If the user is not logged in, show error message and redirect to the login page
        flash("Login and try Again","warning")
        return redirect(url_for('admin.admin_login'))


# [ This route will query and display Hospital users data  ]
@bp.route('/hospitals')
def hospital_data():
    # Check if user is in session and if the user is the ADMIN_NAME
    if 'user' in session and session['user']==var.ADMIN_NAME:
        # Execute SQL query to select all data from hospitaldata table
        query = db.engine.execute('SELECT * FROM hospitaldata')
        # Render the hospitalData.html template with the results of the query
        return render_template('services/hospitalData.html' , query=list(query))
    
    #  If user is not in session or is not the ADMIN_NAME, flash a warning message and redirect to the admin login page
    flash("Login and try Again","warning")
    return redirect(url_for('admin.admin_login'))


# [ This route will query and display users booking data  ]
@bp.route('/userBookings')
def user_data():
    # Check if user is in session and if the user is the ADMIN_NAME
    if 'user' in session and session['user']==var.ADMIN_NAME:
        # Execute SQL query to select all data from userbookings table
        query = db.engine.execute('SELECT * FROM userbookings')
        # Render the userData.html template with the results of the query
        return render_template('services/userData.html' , query=list(query))
    # If user is not in session or is not the ADMIN_NAME, flash a warning message and redirect to the admin login page
    flash("Login and try Again","warning")
    return redirect(url_for('admin.admin_login'))


# [ Admin Logout Route ]
@bp.route("/logout")
def admin_logout():

    # Check if the 'user' key is present in the session and if the value is equal to the value of ADMIN_NAME in the var module
    if 'user' in session and  session['user']==var.ADMIN_NAME:
        # Remove the 'user' key from the session
        session.pop('user')
        # Display a flash message indicating that the admin has successfully logged out
        flash("You are logout admin", "primary")

        # Redirect the user to the admin login page
        return redirect(url_for('admin.admin_login'))
    
    # If the 'user' key is not present in the session or the value is not equal to the value of ADMIN_NAME in the var module
    # Display a flash message indicating that the user needs to log in first
    flash("Login and try Again","warning")
    # Redirect the user to the admin login page
    return redirect(url_for('admin.admin_login'))

