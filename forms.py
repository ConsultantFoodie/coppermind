from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
	email = EmailField('Email Address: ', validators=[DataRequired()])
	course_id = StringField("7 Character Course ID: ", validators=[DataRequired(), Length(min=7, max=7, message="Need exactly 7 characters")])
	take_or_drop = RadioField("Register or Drop:", choices=[(1, "I am registered in this course"), (0, "I am dropping this course")], validators=[DataRequired()])
