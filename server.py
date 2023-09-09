"""Server for sales tracker app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import db, Salesperson, Sale, Customer, connect_to_db

import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/user_dashboard")
def user_dashboard():
    if session["sp_email"]:
        salesperson = crud.get_salesperson_by_username(session["sp_email"])
        sales_list = crud.get_salesperson_sales(salesperson.id)
        sales_total = 0
        for sale in sales_list:
            sales_total +=1

    return render_template("user_dashboard.html", user = salesperson, sales= sales_total)

@app.route("/login", methods=["POST"])
def login():
    """allow user to login"""

    email = request.form.get("username")
    password = request.form.get("password")

    salesperson = Salesperson.get_salesperson_by_username(email)

    if not salesperson or salesperson.password != password:
        flash("The email or password you entered is incorrect. Try again.")

    else:
        session["sp_email"] = salesperson.username
        flash(f"Welcome back, {salesperson.fname}")

    return redirect("/")

@app.route("/register", methods=["POST"])
def register_user():
    """allows a salesperson to create an account"""

    email= request.form.get("new-username")
    password= request.form.get("new-password")
    first_name= request.form.get("fname")
    last_name= request.form.get("lname")

    salesperson = Salesperson.get_salesperson_by_username(email)

    if salesperson:
        flash("Can not use that email to create an account")

    else:
        salesperson= Salesperson.create(first_name, last_name, email, password)
        db.session.add(salesperson)
        db.session.commit()
        flash("Account created! Please login to see your dashboard")

    return redirect('/')

@app.route("/create_sale", methods=["POST"])
def create_sale():
    
    return render_template("user_dashboard.html")

@app.route("/create_customer", methods=["POST"])
def create_customer():
    fname = request.form.get("customer_fname")
    lname = request.form.get("customer_lname")
    email = request.form.get("customer_email")
    phone_num = request.form.get("customer_pnumber")

    new_customer = crud.create_customer(fname, lname, email, phone_num)
    db.session.add(new_customer)
    db.session.commit()
    flash("Customer added")

    return redirect("/user_dashboard")
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    