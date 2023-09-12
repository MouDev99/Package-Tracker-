from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    user_name = StringField("Choose a username", validators=[DataRequired()])
    email = EmailField("Your email address", validators=[DataRequired()])
    password = PasswordField("Type a strong password", validators=[DataRequired()])
    submit = SubmitField("Signup")
