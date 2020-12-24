from flask import Flask, render_template, url_for, redirect, flash, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import models
# import os

'''
	TODO: Add passwords for users so that emails are not misused
		  Add course details section
		  Use CSS if possible
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IAmTheHeroOfAges'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sazed.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return models.Student.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def welcome():
	return render_template("welcome.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		student = models.Student(gender=int(form.gender.data), username=form.name.data.split()[0],
						email=form.email.data, password=hashed_pass)
		print(student)
		try:
			db.session.add(student)
			db.session.commit()
			flash("Pleased to make your acquaitance. Please login to continue.", 'success')
			return redirect(url_for('login'))
		except:
			flash("It seems that email address belongs to someone else. Please use another email address.", "danger")
	
	return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		student = models.Student.query.filter_by(email=form.email.data).first()
		print(student)
		if student and bcrypt.check_password_hash(student.password, form.password.data):
			login_user(student, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("I do not recognise you. Please check your email address and password", "danger")
	return render_template("login.html", form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template("home.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))


if __name__ == "__main__":
	app.run(debug=True)