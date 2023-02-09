'''This code imports the necessary libraries and creates a blueprint for the user functionality.'''
from flask import Blueprint, flash , render_template , request , redirect , url_for
from Flaskapp.models.hospital import *
from Flaskapp.extensions import db
from werkzeug.security import check_password_hash
from flask_login import login_user , login_required, logout_user , current_user


# Creating a blueprint object 'bp' to store the user related functionality
bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )


#Hospital Login 
# This code implements a login route for a hospital. The route is accessible using the GET and POST HTTP methods.
@bp.route('/login' , methods=[ 'GET','POST'])
def hospital_login():

    # If the request method is POST, extract the email and password from the request form
    if request.method=='POST': 
    
        email=request.form.get('email')
        password=request.form.get('password')

        # Query the database for a user with the given email
        user=Hospitaluser.query.filter_by(email=email).first()

        # If a user is found, verify the password
        if user:
            # If the password is correct, log the user in and redirect to the dashboard
            if check_password_hash(user.password , password):
                login_user(user)
                flash('Login Successfull.' , 'success')
                return redirect(url_for('hospital.hospital_dashboard'))
            flash('Please check your login details and try again.' ,'warning')
            return redirect(url_for('hospital.hospital_login')) 
        # If no user is found, show a warning message
        flash('User not registerd' , 'warning')
        return redirect(url_for('hospital.hospital_login'))

    # If the request method is GET, render the login template
    return render_template('hlogin.html')


#Hospital dashboard Page
@bp.route('/dashboard' , methods=['GET' , 'POST'])
@login_required
def hospital_dashboard():

    
    email=current_user.email # get the email of the currently logged in user
    
    # get the first instance of the user in the Hospitaluser table where the email matches
    posts=Hospitaluser.query.filter_by(email=email).first()

    code=posts.hcode # get the hospital code of the current user

    # get the first instance of the hospital data in the Hospitaldata table where the hospital code matches
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    # check if the request method is 'POST'
    if request.method=='POST':              
            # get the values of hcode, hname, nbed, hbed, ibed, and vbed from the form
            hcode=request.form.get('hcode')
            hname=request.form.get('hname')
            nbed=request.form.get('normalbed')
            hbed=request.form.get('hicubeds')
            ibed=request.form.get('icubeds')
            vbed=request.form.get('ventbeds')
            
            hcode=hcode.upper() # convert the hospital code to uppercase

            # get the first instance of the hospital user with the given hospital code
            hospital_user = Hospitaluser.query.filter_by( hcode = hcode ).first()
            # get the first instance of the hospital data with the given hospital code
            hospital_data = Hospitaldata.query.filter_by( hcode = hcode ).first()

            # if the hospital data is already present
            if hospital_data:
                # flash a message to inform the user that the data is already present and they can update it
                flash("Data is already Present you can update it..","primary")
                # render the hdashboard template and pass in the postsdata
                return render_template("hdashboard.html" , postsdata=postsdata)

            # if the hospital user is present
            if hospital_user:
                # create a new instance of the Hospitaldata model with the given parameters
                new_user = Hospitaldata( hcode=hcode, hname=hname, normalbed=nbed , hicubed=hbed , icubed=ibed , vbed=vbed )
                # add the new data to the database 
                db.session.add(new_user)
                # commit the changes to the database
                db.session.commit()
                # flash a success message to inform the user that the data was added
                flash("Data Is Added","success")
                # redirect the user to the hospital dashboard
                return redirect(url_for('hospital.hospital_dashboard'))
            
    # render the hdashboard template and pass in the postsdata
    return render_template('hdashboard.html' , postsdata=postsdata )


# Hospital data update
@bp.route('/update/<string:id>' , methods=['GET' ,'POST'])
@login_required
def hospital_data_update(id):

    # Retrieve the data of the hospital with the given id
    posts=Hospitaldata.query.filter_by(id=id).first() 

    # Check if the request method is POST
    if request.method=="POST":

        # Get the updated data from the form
        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')

        # Update the database with the updated data
        posts.hname = hname
        posts.normalbed = nbed
        posts.hicubed = hbed
        posts.icubed = ibed
        posts.vbed = vbed
            
        db.session.commit()

        # Display a success message and redirect to the hospital dashboard
        flash("Slot Updated","success")
        return redirect(url_for('hospital.hospital_dashboard'))

    # If the request method is GET, render the template for updating the data
    return render_template('hdataUpdate.html' , posts=posts)


# Hospital data delete
# # This code sets up a Flask route that deletes a record in the database associated with a given id. 
@bp.route('/delete/<string:id>') # This sets up a Flask route at '/delete/<id>' where id is a string parameter. 
@login_required  # This decorator ensures that the user must be logged in to access this route. 
def hospital_data_delete(id): # The function takes the id as a parameter and is responsible for deleting the data from the database.

    # This line queries the database for the record with the given id and deletes it. 
    Hospitaldata.query.filter_by(id=id).delete()  
    db.session.commit() # This line commits the changes made to the database. 
    # This line uses the flash function to show a message to the user indicating that the data has been deleted successfully. The "danger" category is used to indicate that this is a negative message. 
    flash("Data Deleted Succesfully" , "danger")

    # This line redirects the user to the hospital dashboard page after the data has been deleted. 
    return redirect(url_for('hospital.hospital_dashboard'))


# Logout form the hospital panel 
@bp.route('/logout')
@login_required
def logout():

    # logout the user using the logout_user function from Flask-Login
    logout_user()
    # Display a success message
    flash("You are logout ", "primary")
    # Redirect the user to the login page
    return redirect(url_for('hospital.hospital_login'))