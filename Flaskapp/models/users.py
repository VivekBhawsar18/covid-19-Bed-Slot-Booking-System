from Flaskapp.extensions import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id    = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(50) , unique=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(50) , unique=True)
    gender = db.Column(db.String(20))
    address = db.Column(db.String(100))
    password=db.Column(db.String(1000))

    def __str__(self) -> str:
        return f"{self.id}-{self.email}-{self.firstname}-{self.lastname}-{self.password}"
    
class Userbookings(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    bedtype=db.Column(db.String(100))
    hcode=db.Column(db.String(20))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(100))
    pphone=db.Column(db.String(100),unique=True)