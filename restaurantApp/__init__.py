from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY']= '45c0ae51e0e13c75a7c4ee3cc059388a'
bcrypt= Bcrypt(app)
login_manager= LoginManager(app)

from restaurantApp import routes