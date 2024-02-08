from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class UserForm(FlaskForm):
    '''defines fields for new user form'''

    username = StringField("username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("password", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("first name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("last name", validators=[InputRequired(), Length(max=30)])

class UserLoginForm(FlaskForm):
    '''defines fields for login form'''

    username = StringField("username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    '''defines fields for feedback form'''

    title = StringField("title", validators=[InputRequired(), Length(max=100)])
    content = TextAreaField("content", validators=[InputRequired()])