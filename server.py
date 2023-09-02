"""Server for sales tracker app"""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db

import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=["POST"])
def login():

@app.route('/register', methods=["POST"])
def register_user():
    




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    