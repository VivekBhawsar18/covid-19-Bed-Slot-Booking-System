from flask import Blueprint, render_template, session
from Flaskapp.models.test import Test
from flask_mail import  Message
from Flaskapp.extensions import mail
from config import AdminCred

bp = Blueprint('test' , __name__ , template_folder='templates')

var = AdminCred()

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

@bp.route('/send/email')
def send_email():
    try:
        msg = Message(
                        'COVID CARE CENTER',
                        sender = var.MAIL_SENDER,
                        recipients = ['info.vivekbhawsar@gmail.com']
                    )
        msg.body = 'Hello Flask message sent from Flask-Mail'
        # msg.html = "<b> COVID CARE CENTER </b>"
        mail.send(msg)
        return 'Mail Sent Check Your Inbox !!!'

    except Exception as e:
        return str(e)

# @bp.context_processor
# def context_processor(value):
#     return dict(key=value , hello='how')

# @bp.route('/session')
# def test_session():
#     try:
#         session['email'] = 'vivekcoder18' 
#         email = session['email']
#         return str(context_processor('hello'))

#     except Exception as e:
#         return str(e)





