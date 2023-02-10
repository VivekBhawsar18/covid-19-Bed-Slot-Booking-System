from flask import Blueprint, render_template, request, session
from Flaskapp.models.test import Test
from flask_mail import  Message
from Flaskapp.extensions import mail
from config import AdminCred
import requests

bp = Blueprint('test' , __name__ , template_folder='templates')

var = AdminCred()

@bp.route('/')
def index():
    return render_template('testIndex.html')
@bp.route('/dbcon')
def db_con():
    try:
        data = Test.query.all()
        # return render_template('dbcon.html',names = data)
        return '<h1>Database connection succesfull!!!</h1>'

    except Exception as e:
        return str(e)

@bp.route('/email' , methods = ['GET' , 'POST'])
def send_email():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            msg = Message(
                            'TEST EMAIL',
                            sender = var.MAIL_SENDER,
                            recipients = [email]
                        )
            msg.body = 'Hello user message sent from Flask-Mail'
            mail.send(msg)
            return '<h1>Mail Sent Check Your Inbox !!!</h1>'

        except Exception as e:
            return str(e)
        
    return render_template('emailTest.html')



@bp.route('/covid')
def covid():
    # Get COVID-19 patient data using the requests library
    data = requests.get("https://api.covidtracking.com/v1/states/current.json").json()

    return render_template('covid.html', data=data)