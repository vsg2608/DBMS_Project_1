from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']= '45c0ae51e0e13c75a7c4ee3cc059388a'

from restaurantApp import routes