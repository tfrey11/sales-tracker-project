"""Server for sales tracker app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import db, Salesperson, Sale, Customer, connect_to_db
from datetime import date
from operator import itemgetter
import os
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/dealer_page")
def dealer_page():
    total_sales_list = crud.get_sales()
    sales_this_month_list = crud.get_dealer_sales()
    t_sales = len(total_sales_list)
    m_sales = len(sales_this_month_list)
    api_k = os.environ['API_KEY']
    sp_sales = {}
    sp_and_sales=[]
    for sale in sales_this_month_list:
        sp_id= sale.sales_person_id
        sp = crud.get_salesperson_by_id(sp_id)

        if sp.fname not in sp_sales.keys():
            sp_sales[sp.fname] = 1
        else:
            sp_sales[sp.fname] += 1

    for key in sp_sales:
        sp_and_sales.append((key, sp_sales[key]))
    
    sp_and_sales.sort(key=lambda x:x[1], reverse=True)


    return render_template("dealer_page.html", total_sales = t_sales, month_sales = m_sales, the_key=api_k, top3=sp_and_sales)

@app.route("/user_dashboard")
def user_dashboard():
    if not session:
        return redirect('/')
    else:
        salesperson = crud.get_salesperson_by_username(session["sp_email"])
        sales_list = crud.get_salesperson_sales(salesperson.id)
        t_date = date.today()
        month= t_date.month
        year = t_date.year
        month_list = crud.get_sales_by_month( month, year, salesperson.id)
        month_sales= 0
        for s in month_list:
            month_sales += 1
        sales_total = 0
        for sale in sales_list:
            sales_total +=1

        return render_template("user_dashboard.html", user = salesperson, sales= sales_total, monthly_sales = month_sales)
 

    

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create_sale", methods=["POST"])
def create_sale():
    c_email = request.form.get("customer_email")
    cus= crud.get_customer_id(c_email)
    seller = crud.get_salesperson_by_username(session["sp_email"])
    make = request.form.get("car_make")
    model = request.form.get("car_model")
    year = request.form.get("car_year")
    price = request.form.get("price")
    date = request.form.get("date")

    new_sale = crud.create_sale(seller.id, cus.id, make, model, year, price, date)
    db.session.add(new_sale)
    db.session.commit()
    flash("New Sale Added!")
    return redirect("user_dashboard")


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
    
@app.route("/sales_this_month_user.json")
def get_sales_this_month():
    """get the sales this month for specific user"""
    monthly_sales = {}
    monthly_sales_list = []
    salesperson = crud.get_salesperson_by_username(session["sp_email"])
    t_date = date.today()
    month= t_date.month
    year = t_date.year
    month_list = crud.get_sales_by_month( month, year, salesperson.id)

    for sale in month_list:
        s_date = sale.sale_date
        if s_date not in monthly_sales:
            monthly_sales[s_date]=1
        else:
            monthly_sales[s_date] += 1
    
    for key in monthly_sales:
        monthly_sales_list.append({'date': key.isoformat(), 'total': monthly_sales[key]})

    monthly_sales_list.sort(key= lambda x:x['date'])

    return jsonify({'data': monthly_sales_list})

@app.route("/sales_this_month_dealer.json")
def dealer_sales():
    dealer_sales = crud.get_dealer_sales()
    monthly_sales = {}
    monthly_sales_list = []
    for sale in dealer_sales:
        s_date = sale.sale_date
        if s_date not in monthly_sales:
            monthly_sales[s_date] = 1
        else:
            monthly_sales[s_date]+=1
    for key in monthly_sales:
        monthly_sales_list.append({'date': key.isoformat(), 'total': monthly_sales[key]})

    monthly_sales_list.sort(key= lambda x:x['date'])

    return jsonify({'data': monthly_sales_list})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    