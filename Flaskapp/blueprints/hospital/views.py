from flask import Blueprint, flash , render_template , request , redirect , url_for
from Flaskapp.models.hospital import *
from Flaskapp.extensions import db
from werkzeug.security import check_password_hash
from flask_login import login_user , login_required, logout_user , current_user


bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )


#Hospital Login 
@bp.route('/login' , methods=[ 'GET','POST'])
def hospital_login():

    if request.method=='POST': 
        # login code goes here
        email=request.form.get('email')
        password=request.form.get('password')

        user=Hospitaluser.query.filter_by(email=email).first()

        # check if the user actually exists
        if user:
            # take the user-supplied password, hash it, and compare it to the hashed password in the database
            if check_password_hash(user.password , password):
                # if the above check passes, then we know the user has the right credentials
                login_user(user)
                flash('Login Successfull.' , 'success')
                return redirect(url_for('hospital.hospital_dashboard'))
            flash('Please check your login details and try again.' ,'warning')
            return redirect(url_for('hospital.hospital_login')) # if the user exist and password is wrong, reload the page
        flash('User not registerd' , 'warning')
        return redirect(url_for('hospital.hospital_login'))# if the user doesn't exist , reload the page


    return render_template('hlogin.html')


#Hospital dashboard Page
@bp.route('/dashboard' , methods=['GET' , 'POST'])
@login_required
def hospital_dashboard():

    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    # Adding Hospital data 
    if request.method=='POST':              
            hcode=request.form.get('hcode')
            hname=request.form.get('hname')
            nbed=request.form.get('normalbed')
            hbed=request.form.get('hicubeds')
            ibed=request.form.get('icubeds')
            vbed=request.form.get('ventbeds')
            hcode=hcode.upper()

            hospital_user = Hospitaluser.query.filter_by( hcode = hcode ).first()
            hospital_data = Hospitaldata.query.filter_by( hcode = hcode ).first()

            # check if the hospital data already exists .
            if hospital_data:
                flash("Data is already Present you can update it..","primary")
                return render_template("hdashboard.html" , postsdata=postsdata)

            # if the above check passes, take the user-supplied data and store it into database.
            if hospital_user:            
                new_user = Hospitaldata( hcode=hcode, hname=hname, normalbed=nbed , hicubed=hbed , icubed=ibed , vbed=vbed ) 
                db.session.add(new_user)
                db.session.commit()
                flash("Data Is Added","success")
                return redirect(url_for('hospital.hospital_dashboard'))
    return render_template('hdashboard.html' , postsdata=postsdata )


# Hospital data update
@bp.route('/update/<string:id>' , methods=['GET' ,'POST'])
@login_required
def hospital_data_update(id):

    posts=Hospitaldata.query.filter_by(id=id).first() # Taking current_user id and bringing data from database

    # if the above check passes, update database entry by user-supplied data .
    if request.method=="POST":

        hname=request.form.get('hname')
        nbed=request.form.get('normalbed')
        hbed=request.form.get('hicubeds')
        ibed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')

        posts.hname = hname
        posts.normalbed = nbed
        posts.hicubed = hbed
        posts.icubed = ibed
        posts.vbed = vbed
            
        db.session.commit()
        flash("Slot Updated","success")
        return redirect(url_for('hospital.hospital_dashboard'))

    
    return render_template('hdataUpdate.html' , posts=posts)


# Hospital data delete 
@bp.route('/delete/<string:id>')
@login_required
def hospital_data_delete(id):

    Hospitaldata.query.filter_by(id=id).delete() # Taking current_user id and delete its all data stored in database
    db.session.commit()
    flash("Data Deleted Succesfully" , "danger")

    return redirect(url_for('hospital.hospital_dashboard'))


# Logout form the hospital panel 
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logout ", "primary")
    return redirect(url_for('hospital.hospital_login'))