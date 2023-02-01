from flask import Blueprint, flash , render_template , request , redirect , url_for
from Flaskapp.models.hospital import *
from Flaskapp.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , login_required, logout_user , current_user

bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )

@bp.route('/login')
def hospital_login():
    return render_template('hlogin.html')


@bp.route('/login' , methods=['POST'])
def hospital_home():
        # login code goes here
        email=request.form.get('email')
        password=request.form.get('password')

        user=Hospitaluser.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not  check_password_hash(user.password,password):

            flash('Please check your login details and try again.' ,'danger')
            return redirect(url_for('hospital.hospital_login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for('hospital.hospital_dashboard' , name=current_user.email))


@bp.route('/dashboard' , methods=['GET' , 'POST'])
@login_required
def hospital_dashboard():

    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

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

            if hospital_data:
                flash("Data is already Present you can update it..","primary")
                return render_template("hdashboard.html" , postsdata=postsdata)

            if hospital_user:            
                new_user = Hospitaldata( hcode=hcode, hname=hname, normalbed=nbed , hicubed=hbed , icubed=ibed , vbed=vbed ) 
                db.session.add(new_user)
                db.session.commit()
                flash("Data Is Added","primary")
                return redirect(url_for('hospital.hospital_dashboard'))

    return render_template('hdashboard.html' , postsdata=postsdata)


@bp.route('/update/<string:id>' , methods=['GET' ,'POST'])
@login_required
def hospital_data_update(id):

    posts=Hospitaldata.query.filter_by(id=id).first()

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
        flash("Slot Updated","info")
        return redirect(url_for('hospital.hospital_dashboard'))


    return render_template('hdataUpdate.html' , posts=posts)


@bp.route('/delete/<string:id>')
@login_required
def hospital_data_delete(id):

    Hospitaldata.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Data Deleted Succesfully" , "danger")

    return redirect(url_for('hospital.hospital_dashboard'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logout ", "primary")
    return redirect(url_for('hospital.hospital_login'))