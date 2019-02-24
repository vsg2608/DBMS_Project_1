from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField, DateTimeField

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
    date        = DateField("Date",format="%Y-%M-%d", validators=[DataRequired()])
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
    rating      = IntegerField('Rating')
    submit      = SubmitField('Search')
    #cuisine   = StringField()
    #cusinineOR    = StringField()
    #Cost range     

class homeSearch(FlaskForm):
    city        = StringField('City:', validators=[DataRequired()])
    submit      = SubmitField('Find Restaurants')

 ####################################################################################

class tableBookingForm(FlaskForm):
    noOfMembers     = IntegerField('Table for',validators=[DataRequired()])
    date        = DateTimeField("Booking Date, Time",format="%Y-%m-%d", validators=[DataRequired()])
    submit          = SubmitField('Book Table')
