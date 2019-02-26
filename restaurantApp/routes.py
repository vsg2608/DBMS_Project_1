import psycopg2 as pg
from flask import Flask, render_template, redirect, flash,url_for, session
from restaurantApp.forms import RegisterationForm, LoginForm, searchForm, UpdateForm, homeSearch, tableBookingForm, ratingForm
from restaurantApp import app, bcrypt, login_manager
import datetime
# dbname = "group_3"
# password = "202-901-602"
# conn = pg.connect(database = dbname, user = "group_3", password=password,  host = "10.17.50.247", port = "5432")
# cur = conn.cursor()

dbname = "project"
password = "Password@123"
conn = pg.connect(database = dbname, user = "postgres", password=password,  host = "13.233.41.140", port = "5432")
cur = conn.cursor()

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = searchForm()
    form.rating.data=0
    form.sortBy.data='rating'
    return render_template('home.html', form=form, title="Home")

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

@app.route('/userAccount',methods=['GET','POST'])
def userAccount():
    if('user' in session):
        form=UpdateForm()
        if form.validate_on_submit():
            print("Updating")
            cur.execute("""UPDATE users SET name= %s, email= %s, dob= %s, gender=%s, address= %s,
                                    locality= %s WHERE user_id= %s;""",
                                    (form.name.data, form.email.data, form.date.data, form.gender.data,
                                    form.address.data, form.locality.data, session['user']))
            conn.commit()
            flash('User details have been updated', 'success')
        cur.execute("SELECT name, email, dob, gender, address, locality FROM users WHERE user_id='"+str(session['user'])+"';")
        user= cur.fetchall()[0]
        form.name.data      = user[0]
        form.email.data     = user[1]
        form.date.data      = user[2]
        form.gender.data    = user[3]
        form.address.data   = user[4]
        form.locality.data  = user[5]   
        image_file= url_for('static', filename='profile_pics/default.jpg')
        return render_template('userAccount.html',title='User Account', user=user, image_file=image_file, form=form)
    else:
        flash('Please login to acess this account', 'danger')
        return redirect(url_for('userLogin'))

@app.route('/bookings', methods=['GET','POST'])
def bookings():
    if('user' in session):
        user_id= session['user']
        query="SELECT rest.restaurant_name, rest.restaurant_id, rest.address, city.locality, transaction.bookedon, transaction.bookedfor, transaction.no_people, transaction.rating , transaction.id  from transaction, rest, city WHERE userid="+str(user_id)+" and rest.restaurant_id= transaction.restid and city.id= rest.localityid ORDER BY transaction.bookedon desc;"
        print(query)
        cur.execute(query)
        bookings= cur.fetchall()
        print(bookings[0])
        rForm= ratingForm()
        image_file= url_for('static', filename='restaurant_pics/default.jpg')
        return render_template('bookings.html', title="Bookings",bookings=bookings, image_file=image_file, ratingForm=rForm)
    else:
        flash('Please login to acess this account', 'danger')
        return redirect(url_for('userLogin'))

@app.route('/rate/<ID>', methods=['GET','POST'])
def rateTransaction(ID):
    print("Transction ID: ",ID)
    rForm= ratingForm()
    if rForm.validate_on_submit():
        print(rForm.rating.data)
        cur.execute("UPDATE transaction SET rating= %s WHERE id = %s",(rForm.rating.data,ID))
        conn.commit()
    return redirect(url_for('bookings'))


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
            flash('Table booked successfully', 'success')
            return redirect(url_for('bookings'))
        else:
            flash('Please login to book the table', 'danger')
            return redirect(url_for('userLogin'))
    return render_template('restaurant.html',title=restaurant[0][0], restaurant=restaurant[0], image_file=image_file, form=form)


@app.route('/search', methods=['GET','POST'])
def search():
    form= searchForm()
    if form.validate_on_submit():
        print(form.rating.data==None)
        if(form.cuisine.data!=""):
            query="SELECT distinct restaurant_name,address, cuisines, averagecost_for_two, currency, rest.aggregate_rating, restaurant_id, ratings.rating_color from rest, city, cuisine,rest_cuisine, ratings WHERE rest.localityid=city.id and lower(city.city)=lower('"+str(form.city.data)+"') and ratings.aggregate_rating = rest.aggregate_rating "
        else:
            query="SELECT distinct restaurant_name,address, cuisines, averagecost_for_two, currency, rest.aggregate_rating, restaurant_id, ratings.rating_color from rest, city, ratings WHERE rest.localityid=city.id and lower(city.city)=lower('"+str(form.city.data)+"') and ratings.aggregate_rating = rest.aggregate_rating "
        if(form.restaurantName.data!=""):
            query+=" and lower(rest.restaurant_name) like lower('%" + form.restaurantName.data + "%') "
        if(form.locality.data!=""):
            query+=" and lower(city.locality) like lower('%" + form.locality.data + "%') "
        if(form.rating.data!="" and form.rating.data!=None):
            query+=" and rest.aggregate_rating>= "+str(form.rating.data)
        cuisines=form.cuisine.data
        cuisines=cuisines.split(",")
        temp="'"
        for cuisine in cuisines:
            cuisine=cuisine.lower()
            cuisine=cuisine.strip()
            temp+=cuisine+"','"
        cuisines= temp[:len(temp)-2]
        # cuisines="'japanese','korean'"
        # and_or=False
        print(cuisines)
        if(form.cuisine.data!=""):
            query+= " and rest.restaurant_id= rest_cuisine.rest_id and cuisine.cuisine_code= rest_cuisine.cuisine_code and lower(cuisine.cuisine) in ("+cuisines+") "
        

        if(form.sortBy.data=='rating'):
            query+= "ORDER BY rest.aggregate_rating desc"
        elif(form.sortBy.data=='price'):
            query+= "ORDER BY rest.averagecost_for_two"
        elif(form.sortBy.data=='restName'):
            query+= "ORDER BY rest.restaurant_name"

        print(query)
        cur.execute(query+";")
        restaurants= cur.fetchall()
    else:
        form.rating.data=0
        form.sortBy.data='rating'
        cur.execute("""SELECT restaurant_name,address, cuisines, averagecost_for_two, currency, rest.aggregate_rating, restaurant_id, ratings.rating_color FROM rest, ratings WHERE ratings.aggregate_rating = rest.aggregate_rating LIMIT 10;""")
        restaurants= cur.fetchall()
    return render_template('search.html',title='Find Restaurant',restaurants=restaurants, form=form)

@app.route('/setCurrency', methods=['GET','POST'])
def setCurrency():
    session['currency']='Pounds()'
    return 'Curency set to ' + session['currency']

@app.route('/getCurrency', methods=['GET','POST'])
def getCurrency():
    cur.execute("SELECT * from cur_conv;")
    currencies= cur.fetchall()
    print(currencies)
    return session['currency'] or None