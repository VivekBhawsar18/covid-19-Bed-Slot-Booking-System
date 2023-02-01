from Flaskapp.extensions import db
from flask_login import UserMixin

class Hospitaluser(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))