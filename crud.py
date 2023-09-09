"""CRUD operations for db"""

from datetime import datetime
from model import db, Salesperson, Sale, Customer, connect_to_db

def create_salesperson(first_name, last_name, email, pword,):
    """create and return a new salesperson"""
    salesperson = Salesperson(fname=first_name, lname=last_name, username=email, password=pword )

    return salesperson

def get_salespeople():
    """return all salespeople"""

    return Salesperson.query.all()

def get_salesperson_by_username(username):
    """return a salesperson by username"""

    return Salesperson.query.filter(Salesperson.username == username).first()

def create_sale(seller_id, cus_id, c_make, c_model, c_year, s_price, s_date):
    """create and return a new sale"""
    n_sale= Sale(sales_person_id=seller_id, customer_id=cus_id, car_make=c_make, car_model=c_model,
                 car_year=c_year, sell_price=s_price, sale_date=s_date)
    
    return n_sale

def get_sales():
    """Return all sales"""

    return Sale.query.all()

def get_salesperson_sales(seller_id):
    """return all sales by specific salesperson"""
    return Sale.query.filter(Sale.sales_person_id == seller_id)

def create_customer(fname, lname, email, pnumber):
    """Create and return new customer"""

    n_customer = Customer(customer_fname = fname, customer_lname = lname,
                          customer_email = email, customer_phone_number = pnumber)
    
    return n_customer

def get_customer_by_id(c_id):
    """Return customer by id"""

    return Customer.query.filter(Customer.id == c_id).first()




if __name__ == "__main__":
    from server import app
    connect_to_db
    