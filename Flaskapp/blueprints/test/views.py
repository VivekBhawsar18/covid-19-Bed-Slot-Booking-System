from flask import Blueprint, render_template
from Flaskapp.models.test import Test

bp = Blueprint('test' , __name__ )

@bp.route('/')
def index():
    return "<h1>Index page of Test blueprint</h1>"

@bp.route('/dbcon')
def db_con():
    try:
        data = Test.query.all()
        return render_template('dbcon.html',names = data)

    except Exception as e:
        return str(e)

