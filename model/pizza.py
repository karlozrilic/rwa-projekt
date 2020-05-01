from . import db

class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(50))
    cijena = db.Column(db.String(50))
    sastojci = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())