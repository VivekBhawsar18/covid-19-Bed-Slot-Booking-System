import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class MailConfig:
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT='465'
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.environ.get('GMAIL_ACCOUNT')
    MAIL_PASSWORD=os.environ.get('GAMIL_ACC_PASS')


class AdminCred:
    ADMIN_NAME = os.environ.get('ADMIN_NAME')
    ADMIN_PWD  = os.environ.get('ADMIN_PASS')
    MAIL_SENDER = os.environ.get('GMAIL_ACCOUNT')