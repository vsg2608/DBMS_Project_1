import psycopg2 as pg
from flask import Flask, render_template, redirect, flash,url_for
from forms import RegisterationForm, LoginForm, searchForm
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

@app.route('/search', methods=['GET','POST'])
def search():
   cur.execute("""SELECT restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating FROM rest LIMIT 10;""")
   restaurants= cur.fetchall()
   form= searchForm()
   if form.validate_on_submit():
      print(form.locality.data)
      print(form.rating.data)
      query="SELECT distinct restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating from rest, city, cuisine,rest_cuisine WHERE rest.localityid=city.id and lower(city.city)=lower('"+str(form.city.data)+"') "
      if(form.restaurantName.data!=""):
         query+=" and lower(rest.restaurant_name) like lower('%" + form.restaurantName.data + "%') "
      if(form.locality.data!=""):
         query+=" and lower(city.locality) like lower('%" + form.locality.data + "%') "
      if(form.rating.data!=""):
         query+=" and rest.aggregate_rating>= "+str(form.rating.data)
      cuisines="'japanese','korean'"
      and_or=False
      if(cuisines!=""):
        query+= " and rest.restaurant_id= rest_cuisine.rest_id and cuisine.cuisine_code= rest_cuisine.cuisine_code and lower(cuisine.cuisine) in ("+cuisines+") "

      sortbyRating= False
      sortbyRestName= False
      sortbyPrice= True
      if(sortbyPrice):
         query+= "ORDER BY rest.aggregate_rating desc"
      print(query)
      cur.execute(query+";")
      restaurants= cur.fetchall()
   return render_template('search.html',title='Find Restaurant',restaurants=restaurants, form=form)
   
@app.route('/userRegister', methods=['GET','POST'])
def userRegister():
   form= RegisterationForm()
   if form.validate_on_submit():
      date="2018-12-30"
      gender="M"
      address="153 Phulkian Enclave, New Delhi"
      locality="Hauz Khas"
      name= form.name.data
      email=form.email.data
      password=form.password.data
      cur.execute("Select email from users where email= '"+email+"';")
      Email=cur.fetchall()
      if(Email==[]):
         flash(f'Account created for {form.name.data}!', 'success')
         cur.execute("INSERT into users (password, name, email, dob, gender, address, locality) values " \
                     "(%s, %s, %s, %s, %s,%s,%s);", (password,name, email, date, gender, address, locality))
         conn.commit()
         return redirect(url_for('home'))
      else:
         flash('Email already exists!!!!', 'danger')
      
   return render_template('userRegister.html',title='User Register', form=form)

@app.route('/userLogin', methods=['GET','POST'])
def userLogin():
   form= LoginForm()
   print(form.email.data)
   if form.validate_on_submit():
      cur.execute("select password from users where email='"+str(form.email.data)+"';")
      password=cur.fetchall()
      if([]==password):
         flash('Email not found. Please check your email', 'danger')
      else:
         password=password[0][0]
         if form.password.data == password:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
         else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
   return render_template('userlogin.html',title='User Login', form=form)

if __name__ == '__main__':
   app.run(debug=True)