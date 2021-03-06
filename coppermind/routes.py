from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from coppermind.main import app, db, bcrypt
from coppermind.forms import RegistrationForm, LoginForm, CourseForm, WorkForm, ForgetForm
from coppermind.models import Student, Course, Signup, Deadline
import json
from os import environ as env
import requests
import datetime

course_list = []
with open('coppermind/courses.json', 'r') as file:
	course_list = json.load(file)

course_list.sort()

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
			login_user(student)
			next_page = request.values.get('next')
			print(request)
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("I do not recognise you. Please check your email address and password. Have you registered?", "danger")
	return render_template("login.html", form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==current_user.id).order_by(Signup.course_id).all()
	print(courses)
	return render_template("home.html", courses=courses)


@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
	form = CourseForm()
	if form.validate_on_submit():
		form.course_id.data = form.course_id.data.upper()
		print(form.course_id.data, form.add_drop.data)
		if form.add_drop.data == '1':
			student = Student.query.filter_by(email=current_user.email).first()
			course = Course.query.filter_by(course_name=form.course_id.data).first()
			print(course)
			if form.course_id.data not in course_list:
				flash('Please choose a valid course.','danger')
				return redirect(url_for('courses'))
			if not course:
				course = Course(course_name=form.course_id.data)
				db.session.add(course)

			checker = Signup.query.filter_by(course_id=course.id, student_id=student.id).first()
			if not checker:
				student.courses.append(course)
				course.students.append(student)

			db.session.commit()

		elif form.add_drop.data == '0':
			student = Student.query.filter_by(email=current_user.email).first()
			course = Course.query.filter_by(course_name=form.course_id.data).first()
			if student and course:
				print(Course.query.all())
				print("_________")
				print(Student.query.all())
				print("_________")
				print(Signup.query.all())
				signed_up = Signup.query.filter_by(course_id=course.id, student_id=student.id).first()
				if signed_up:
					db.session.delete(signed_up)
					db.session.commit()
		flash("I have done as you requested.", "success")
		return redirect(url_for('courses'))
	else:
		if "course_id" in form.errors.keys():
			flash("I seem to have trouble doing this.Can you check the Course ID? It should be at least 7 characters long.", "danger")


	return render_template("courses.html", form=form, courses=course_list)

@app.route("/work", methods=['GET', 'POST'])
@login_required
def work():
	form = WorkForm()
	today = datetime.date.today()
	if form.validate_on_submit():
		print(form.submit_date.data, form.submit_time.data)
		courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==current_user.id).order_by(Signup.course_id).all()
		student_course_list = [course.course_name for course in courses]
		checker = Course.query.filter_by(course_name=form.course_id.data).first()

		if (form.course_id.data in student_course_list) and checker:
			deadline = Deadline(work_type=int(form.work_type.data), brief_desc=form.brief_desc.data, details=form.details.data, submit_date=form.submit_date.data, submit_time=form.submit_time.data)
			checker.deadlines.append(deadline)
			db.session.commit()
			flash("Added deadline.", "success")
		else:
			flash("Please register yourself in this course first.", "danger")
		return redirect(url_for("work"))
	else:
		print(form.errors)
		print(form.submit_date.data)
	return render_template("work.html", form=form, courses=course_list, today=today)

@app.route("/deadlines/<int:course_id>", methods=['GET', 'POST'])
@login_required
def deadlines(course_id):
	course = Course.query.get_or_404(int(course_id))
	courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==current_user.id).order_by(Signup.course_id).all()
	student_course_list = [course.id for course in courses]
	if course_id not in student_course_list:
		flash("Please register yourself in this course to view its deadlines.", "danger")
		return redirect(url_for('home'))
	display = Deadline.query.filter_by(course=course_id).all()
	return render_template("deadlines.html", display=display, course=course)

@app.route("/deadlines/<int:course_id>/<int:deadline_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(course_id, deadline_id):
	deadline = Deadline.query.get_or_404(int(deadline_id))
	courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==current_user.id).order_by(Signup.course_id).all()
	student_course_list = [course.id for course in courses]
	if course_id not in student_course_list:
		flash("Please register yourself in this course to change its deadlines.", "danger")
		return redirect(url_for('home'))
	db.session.delete(deadline)
	db.session.commit()
	return redirect(url_for('deadlines', course_id=course_id))

@app.route("/forget", methods=['GET', 'POST'])
@login_required
def forget():
	form = ForgetForm()
	if form.validate_on_submit():
		if form.confirm_field.data == "ODIUM REIGNS":
			student = Student.query.filter_by(email=current_user.email).first()
			db.session.delete(student)
			db.session.commit()
			flash("It has been an honour serving you.", "info")
			return redirect(url_for('welcome'))
		else:
			flash('Please confirm your decision by typing the phrase.', "danger")
			return redirect(url_for('forget'))

	return render_template("forget.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))
