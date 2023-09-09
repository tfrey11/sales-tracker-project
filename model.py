"""Models for sales tracker app"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Salesperson(db.Model):
    """A salesperson"""

    __tablename__ = "salespeople"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

    sales = db.relationship("Sale", back_populates="salesperson")


    def __repr__(self):
        return f"<Salesperson id={self.id} name={self.fname} {self.lname}>"
    
    @classmethod
    def create(cls, fname, lname, username, password):
        """create and return a new salesperson"""
        return cls(fname=fname, lname=lname, username=username, password=password)
    
    @classmethod
    def get_salesperson_by_username(cls, username):
        return cls.query.filter(Salesperson.username == username).first()
    
class Sale(db.Model):
    """A sale"""

    __tablename__ = "sales"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sales_person_id = db.Column(db.Integer, db.ForeignKey("salespeople.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    car_make = db.Column(db.String)
    car_model = db.Column(db.String)
    car_year = db.Column(db.Integer)
    sell_price = db.Column(db.Float)
    sale_date = db.Column(db.Date)

    customers = db.relationship("Customer", back_populates="purchases")
    salesperson = db.relationship("Salesperson", back_populates="sales")

    def __repr__(self):
        return f"<Sale id={self.id} salesperson={self.sales_person_id} date={self.sale_date}>"
    
class Customer(db.Model):
    """A customer"""

    __tablename__ = "customers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_fname = db.Column(db.String)
    customer_lname = db.Column(db.String)
    customer_email = db.Column(db.String)
    customer_phone_number = db.Column(db.String)

    purchases = db.relationship("Sale", back_populates="customers")

    def __repr__(self):
        return f"<Customer customer_id={self.id} customer_name={self.customer_fname} {self.customer_lname}>"
    
    

def connect_to_db(flask_app, db_uri="postgresql:///salesdata", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)