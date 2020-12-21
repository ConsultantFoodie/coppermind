from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length
# from flask_sqlalchemy import SQLALchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'IAmTheHeroOfAges'
# app.config['SQLALCHEMY_DTATABASE_URI'] = 'sqlite:///manager.db'
# db = SQLALchemy(app)

class MyForm(FlaskForm):
	email = EmailField('Email Address: ', validators=[DataRequired()])
	course_id = StringField("7 Character Course ID: ", validators=[DataRequired(), Length(min=7, max=7, message="Need exactly 7 characters")])
	take_or_drop = RadioField("Register or Drop:", choices=[(1, "I am registered in this course"), (0, "I am dropping this course")], validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
	form = MyForm()
	if form.validate_on_submit():
		print(form.take_or_drop.data, type(form.take_or_drop.data))
		print(form.email.data, form.course_id.data,  ("Registered" if form.take_or_drop.data == '1' else "Dropped"))
		return redirect(url_for('index'))

	return render_template("index.html", form=form)

if __name__ == "__main__":
	app.run(debug=True)