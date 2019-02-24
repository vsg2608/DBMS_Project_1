import psycopg2 as pg
from flask import Flask, render_template, redirect, flash,url_for, session
from restaurantApp.forms import RegisterationForm, LoginForm, searchForm, UpdateForm, homeSearch, tableBookingForm
from restaurantApp import app, bcrypt, login_manager
import datetime
dbname = "project"
password = "Password@123"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "13.233.41.140", port = "5432")
cur = conn.cursor()

@app.route('/')
@app.route('/home')
def home():
    form = homeSearch()
    if 'user' in session:
        bookings= getBookingDetails(session['user'])
        print(bookings)
    else:
        bookings=[]
    image_file= url_for('static', filename='restaurant_pics/default.jpg')
    return render_template('home.html', form=form, title="Home",bookings=bookings, image_file=image_file)

@app.route('/about')
def about():
    image_file= url_for('static', filename='profile_pics/default.jpg')
    return render_template('about.html',title='About', image_file=image_file)

######################################### Login Logout routes ###############################################
@app.route('/userRegister', methods=['GET','POST'])
def userRegister():
    form= RegisterationForm()
    if form.validate_on_submit():
        hashedPassword= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        date= form.date.data    
        gender= form.gender.data   
        address=form.address.data
        locality= form.locality.data
        name= form.name.data
        email=form.email.data
        print(name, email, gender, date, address, locality)
        cur.execute("Select email from users where email= '"+email+"';")
        Email=cur.fetchall()
        if(Email==[]):
            flash(f'Account created for {form.name.data}!', 'success')
            cur.execute("INSERT into users (password, name, email, dob, gender, address, locality) values " \
                        "(%s, %s, %s, %s, %s,%s,%s);", (hashedPassword,name, email, date, gender, address, locality))
            conn.commit()
            return redirect(url_for('home'))
        else:
            flash('Email already exists!!!!', 'danger')
        
    return render_template('userRegister.html',title='User Register', form=form)

@app.route('/userLogin', methods=['GET','POST'])
def userLogin():
    form= LoginForm()
    if form.validate_on_submit():
        cur.execute("select password, user_id from users where email='"+str(form.email.data)+"';")
        userDetails=cur.fetchall()
        if([]==userDetails):
            flash('Email not found. Please check your email', 'danger')
        else:
            hashedPassword=userDetails[0][0]
            if bcrypt.check_password_hash(hashedPassword,form.password.data):
                flash('You have been logged in!', 'success')
                session['user']=userDetails[0][1]
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('userlogin.html',title='User Login', form=form)

@app.route('/userLogout')
def userLogout():
    session.pop('user', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/userAccount')
def userAccount():
    if('user' in session):
        form=UpdateForm()
        cur.execute("SELECT name, email FROM users WHERE user_id='"+str(session['user'])+"';")
        user= cur.fetchall()[0]
        image_file= url_for('static', filename='profile_pics/default.jpg')
        return render_template('userAccount.html',title='User Account', user=user, image_file=image_file, form=form)
    else:
        flash('Please login to acess this account', 'danger')
        return redirect(url_for('userLogin'))


########################################### Restaurant routes #####################################
@app.route('/find/<ID>', methods=['GET','POST'])
def findRestaurant(ID):
    query="SELECT restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating FROM rest WHERE restaurant_id= '"+str(ID)+"';"
    cur.execute(query)
    restaurant= cur.fetchall()
    image_file= url_for('static', filename='restaurant_pics/default.jpg')
    form= tableBookingForm()
    
    if form.validate_on_submit():
        if('user' in session):
            userid= session['user']
            restid= ID
            bookedon= datetime.datetime.now()
            bookedfor= form.date.data
            no_people= form.noOfMembers.data
            cur.execute("INSERT into transaction (userid, restid, bookedon, bookedfor, no_people ) values " \
                        "(%s, %s, %s, %s, %s);", (userid, restid, bookedon, bookedfor, no_people))
            conn.commit()
        else:
            flash('Please login to book the table', 'danger')
        return redirect(url_for('userLogin'))
    return render_template('restaurant.html',title=restaurant[0][0], restaurant=restaurant[0], image_file=image_file, form=form)


@app.route('/search', methods=['GET','POST'])
def search():
   cur.execute("""SELECT restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating, restaurant_id FROM rest LIMIT 10;""")
   restaurants= cur.fetchall()
   form= searchForm()
   if form.validate_on_submit():
        print(form.rating.data==None)
        query="SELECT distinct restaurant_name,address, cuisines, averagecost_for_two, currency, aggregate_rating, restaurant_id from rest, city, cuisine,rest_cuisine WHERE rest.localityid=city.id and lower(city.city)=lower('"+str(form.city.data)+"') "
        if(form.restaurantName.data!=""):
            query+=" and lower(rest.restaurant_name) like lower('%" + form.restaurantName.data + "%') "
        if(form.locality.data!=""):
            query+=" and lower(city.locality) like lower('%" + form.locality.data + "%') "
        if(form.rating.data!="" and form.rating.data!=None):
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

def getBookingDetails(user_id):
    cur.execute("SELECT rest.restaurant_name, rest.address, city.locality, transaction.bookedfor, transaction.no_people, transaction.rating from transaction, rest, city WHERE userid="+str(user_id)+" and rest.restaurant_id= transaction.restid and city.id= rest.localityid;")
    return cur.fetchall()