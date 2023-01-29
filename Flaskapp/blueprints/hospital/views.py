from flask import Blueprint , render_template , request , redirect , url_for

bp = Blueprint('hospital' , __name__ , static_folder='static' , template_folder='templates' )

@bp.route('/login')
def hospital_login():
    return render_template('hlogin.html')