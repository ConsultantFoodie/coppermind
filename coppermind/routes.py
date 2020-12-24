from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from coppermind.main import app, db, bcrypt
from coppermind.forms import RegistrationForm, LoginForm, CourseForm
from coppermind.models import Student


@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome')
def welcome():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	return render_template("welcome.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		student = Student(gender=int(form.gender.data), username=form.name.data.split()[0],
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
	else:
		if 'gender' in form.errors.keys():
			flash("Please choose your title(gender)!", "danger")
		if 'confirm_pass' in form.errors.keys():
			flash("Passwords did not match. Please try again.", "danger")
		return render_template("register.html", form=form)

	return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		student = Student.query.filter_by(email=form.email.data).first()
		print(student)
		if student and bcrypt.check_password_hash(student.password, form.password.data):
			login_user(student, remember=form.remember.data)
			next_page = request.values.get('next')
			print(request)
			# if request.method == 'POST':
			# 	session['email'] = request.form.get['email']
			# 	print(url_for())
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("I do not recognise you. Please check your email address and password. Have you registered?", "danger")
	return render_template("login.html", form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", user_courses=current_user.courses.split(';'))

@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
	form = CourseForm()
	if form.validate_on_submit():
		print(form.course_id.data, form.add_drop.data)
		flash("I have done as you requested.", "success")
		return redirect(url_for('courses'))
	else:
		if "course_id" in form.errors.keys():
			print(form.errors)
			flash("I seem to have trouble doing this. Can you check the Course ID? It should be exactly 7 characters long.", "danger")
			return redirect(url_for('courses'))

	print(form.errors)
	return render_template("courses.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))
