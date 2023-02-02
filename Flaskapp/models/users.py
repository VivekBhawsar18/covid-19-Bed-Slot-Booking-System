from Flaskapp.extensions import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id    = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(50) , unique=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    dob = db.Column(db.String(20))
    password=db.Column(db.String(1000))

    def __str__(self) -> str:
        return f"{self.id}-{self.email}-{self.firstname}-{self.lastname}-{self.dob}-{self.password}"