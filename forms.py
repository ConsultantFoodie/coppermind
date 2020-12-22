from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
	gender = RadioField("Can I ask about your title?", choices=[(0, "Lord"), (1, "Lady"), (2, "Noble")], validators=[DataRequired()])
	name = StringField("How should I address you?", validators=[DataRequired()])
	email = EmailField("Where should I email my reminders?", validators=[DataRequired()])
	password = PasswordField("What password should we set?", validators=[DataRequired()])
	confirm_pass = PasswordField("Please confirm the password with me.", validators=[DataRequired(), EqualTo('password')])
	# submit = SubmitField('Enlist me in your service.')

class LoginForm(FlaskForm):
	email = EmailField("Please tell me your mailing address.", validators=[DataRequired()])
	password = PasswordField("Please tell me the password to verify your identity.", validators=[DataRequired()])
	remember = BooleanField('Should I remember you?')
	# submit = SubmitField('Allow me to assist you.')