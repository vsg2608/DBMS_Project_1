from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterationForm(FlaskForm):
    name        = StringField('Name',
                    validators=[DataRequired(),Length(min=2, max=20)])
    email       = StringField('Email',validators=[DataRequired(),Email()])
    password    = PasswordField('Password',validators=[DataRequired()])
    date        = DateField("Date",format="%Y-%M-%d", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email       = StringField('Email',validators=[DataRequired(),Email()])
    password    = PasswordField('Password',validators=[DataRequired()])
    remember    = BooleanField('Remember Me')
    submit      = SubmitField('Log In')

class searchForm(FlaskForm):
    city        = StringField('City',
                    validators=[DataRequired(),Length(min=2, max=20)])
    restaurantName= StringField('Restaurant Name')
    locality    = StringField('Locality')
    rating      = IntegerField('Rating')
    submit      = SubmitField('Search')
    #cuisine   = StringField()
    #cusinineOR    = StringField()
    #Cost range     