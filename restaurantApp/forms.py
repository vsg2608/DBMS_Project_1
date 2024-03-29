from flask_wtf import FlaskForm
from wtforms import StringField,SelectField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from wtforms.fields.html5 import DateField, DateTimeField, DateTimeLocalField

from datetime import datetime, timedelta
class RegisterationForm(FlaskForm):
    name        = StringField('Name',
                    validators=[DataRequired(),Length(min=2, max=20)])
    email       = StringField('Email',validators=[DataRequired(),Email()])
    password    = PasswordField('Password',validators=[DataRequired()])
    date        = DateField("Date of Birth",format="%Y-%m-%d", validators=[DataRequired()])
    gender      = RadioField("Gender", choices=[('M','Male'),('F','Female')])
    address     = TextAreaField("Address", validators=[DataRequired()])
    locality    = StringField("Locality", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Sign Up')

class UpdateForm(FlaskForm):
    name        = StringField('Name',
                    validators=[DataRequired(),Length(min=2, max=20)])
    email       = StringField('Email',validators=[DataRequired(),Email()])
    date        = DateField("Date of Birth",format="%Y-%m-%d", validators=[DataRequired()])
    gender      = RadioField("Gender", choices=[('M','Male'),('F','Female')])
    address     = TextAreaField("Address", validators=[DataRequired()])
    locality    = StringField("Locality", validators=[DataRequired()])
    submit      = SubmitField('Update')

class LoginForm(FlaskForm):
    email       = StringField('Email',validators=[DataRequired(),Email()])
    password    = PasswordField('Password',validators=[DataRequired()])
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Log In')

######################################################################################################

class searchForm(FlaskForm):
    city        = StringField('City',
                    validators=[DataRequired()])
    restaurantName= StringField('Restaurant Name')
    locality    = StringField('Locality')
    rating      = IntegerField("Rating", validators=[NumberRange(min=0, max=5, message="Rating should be between 0 and 5")])
    submit      = SubmitField('Search')
    cuisine     = StringField()
    sortBy      = RadioField("Sort By", choices=[('rating','Rating'),('price','Price'),('restName','Restaurant Name')])
       

class homeSearch(FlaskForm):
    city        = StringField('City:', validators=[DataRequired()])
    submit      = SubmitField('Find Restaurants')

#######################################################################################################

class tableBookingForm(FlaskForm):
    noOfMembers     = IntegerField('Table for',validators=[DataRequired()])
    date            = DateTimeField(label='Booking Date & Time (Upto 7 days from now)',validators=[DataRequired()],format = "%D %H:%M",default= datetime.now()+timedelta(days=1))
    submit          = SubmitField('Book Table')

class ratingForm(FlaskForm):
    rating      = IntegerField("Rating", validators=[DataRequired(), NumberRange(min=0, max=5, message="Rating should be between 0 and 5")])
    submit      = SubmitField('Rate')

########################################################################################################

CURRENCY_CHOICES = [('AL', 'Alabama'),('AK','Alaska')]

class currencyForm(FlaskForm):
    currency = SelectField(label='State', choices=CURRENCY_CHOICES)

