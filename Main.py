import psycopg2 as pg
from flask import Flask, render_template, redirect, flash
from forms import RegisterationForm, LoginForm
import os
import sys

dbname = "project"
password = "Password@123"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "13.233.41.140", port = "5432")
cur = conn.cursor()

app = Flask(__name__)
app.config['SECRET_KEY']= '45c0ae51e0e13c75a7c4ee3cc059388a'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
   return render_template('about.html',title='About')

@app.route('/search')
def search():
   cur.execute("""SELECT restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating FROM rest LIMIT 10;""")
   restaurants= cur.fetchall()
   print(restaurants[0][0])
   return render_template('search.html',title='Find Restaurant',restaurants=restaurants)
   
@app.route('/userRegister', methods=['GET','POST'])
def userRegister():
   form= RegisterationForm()
   if form.validate_on_submit():
      flash(f'Accound Created for { form.username.data}!', 'success')
      return redirect(url_for('home'))
   return render_template('userRegister.html',title='User Register', form=form)

@app.route('/userLogin')
def userLogin():
   form= LoginForm()
   return render_template('userlogin.html',title='User Login', form=form)

if __name__ == '__main__':
   app.run(debug=True)