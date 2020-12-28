from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
	gender = RadioField("What is your title amongst the other nobility?", choices=[(0, "Lord"), (1, "Lady"), (2, "Noble")], validators=[DataRequired()])
	name = StringField("How should I address you?", validators=[DataRequired()])
	email = EmailField("Where should I send my reminders?", validators=[DataRequired()])
	password = PasswordField("It would be prudent to discuss a code word. Do you have suggestions?", validators=[DataRequired()])
	confirm_pass = PasswordField("Please confirm the code word with me.", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Enlist me in your service.')

class LoginForm(FlaskForm):
	email = EmailField("Please tell me your mailing address.", validators=[DataRequired()])
	password = PasswordField("Please tell me the password to verify your identity.", validators=[DataRequired()])
	remember = BooleanField('Should I remember you?')
	submit = SubmitField('Allow me to assist you.')

class CourseForm(FlaskForm):
	course_id = StringField("Which course would you like to talk about?", validators=[DataRequired(), Length(min=7, max=7)])
	add_drop = RadioField("Do you wish to add this course? Or are you dropping it?", choices=[(1, "Add me to this course."), (0, "Drop me from this course.")], validators=[DataRequired()])
	submit = SubmitField("That's it for now, Sazed.")

class WorkForm(FlaskForm):
	course_id = StringField("Which course would you like to talk about?", validators=[DataRequired(), Length(min=7, max=7)])
	submit_date = DateField("When is the deadline?", format='%Y-%m-%d', validators=[DataRequired()])
	submit_time = TimeField("When is the deadline?", format='%H:%M', validators=[DataRequired()])	
	work_type = RadioField("What type of deadline is it?", choices=[(1, "Quiz"), (2, "Test"), (3, "Submission"), (4, "Project"), (5, "Viva"), (0, "Other")], validators=[DataRequired()])
	brief_desc = StringField("Please give a brief description. (Max 100 characters)", validators=[DataRequired(), Length(max=100)])
	details = TextAreaField("Any more details? (Max 750 characters)", validators=[Length(max=750)])
	submit = SubmitField("Remember this for me.")