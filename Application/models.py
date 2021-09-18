from Application import db
from datetime import datetime
from sqlalchemy import inspect

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.username

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone=db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    
    
    def __repr__(self):
        return '<Customer %r>' % self.username

class Listing(db.Model):
    __bind_key__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price=db.Column(db.String(10), nullable=False)
    discount=db.Column(db.Integer, default=0)
    description=db.Column(db.Text, nullable=False)
    pub_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   
    image_1=db.Column(db.String(150), nullable=False, default="image.jpg")
    image_2=db.Column(db.String(150), nullable=False, default="image.jpg")
    image_3=db.Column(db.String(150), nullable=False, default="image.jpg")

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }   

    def __repr__(self):
        return '<AddListing %r>' % self.name



class Booking(db.Model):
    __bind_key__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    days=db.Column(db.Integer, default=0)
    date_in=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_out=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  

    active=db.Column(db.Boolean, nullable=False, default=True)
    visited=db.Column(db.Boolean, nullable=False, default=False)

    paid=db.Column(db.Boolean, nullable=False, default=False)
    payment_no=db.Column(db.String(15), nullable=False, default="")
    amount_paid=db.Column(db.String(10), nullable=False, default="")

    user_id=db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user=db.relationship("Customer", backref=db.backref("owner"))

    listing_id=db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    listing=db.relationship('Listing', backref=db.backref("listings"))  
    
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }   
        
    def __repr__(self):
        return '<Bookings %r>' % str(self.days)

db.create_all()