from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from coppermind.main import app, db, bcrypt
from coppermind.forms import RegistrationForm, LoginForm, CourseForm, WorkForm
from coppermind.models import Student, Course, Signup, Deadline


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
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("I do not recognise you. Please check your email address and password. Have you registered?", "danger")
	return render_template("login.html", form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
	courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==current_user.id).order_by(Signup.course_id).all()
	# courses = courses.with_entities()
	print(courses)
	return render_template("home.html", courses=courses)


'''
	Add list of all courses from Kronos.
'''

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
			print("ALL: ", Course.query.all())
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
			flash("I seem to have trouble doing this. Can you check the Course ID? It should be exactly 7 characters long.", "danger")


	return render_template("courses.html", form=form)

'''
	TODO
	Store input date and time in database
'''

@app.route("/work", methods=['GET', 'POST'])
def work():
	form = WorkForm()
	if form.validate_on_submit():
		form.course_id.data = form.course_id.data.upper()
		print(form.course_id.data, form.submit_date.data, form.submit_time.data)
		checker = Course.query.filter_by(course_name=form.course_id.data).first()
		if checker:
			deadline = Deadline(work_type=int(form.work_type.data), brief_desc=form.brief_desc.data, details=form.details.data)
			checker.deadlines.append(deadline)
			db.session.commit()
			flash("Added deadline.", "success")
		else:
			flash("Course does not exist", "danger")
		return redirect(url_for("work"))
	else:
		print(form.errors)
		print(form.submit_date.data)
	return render_template("work.html", form=form)

@app.route("/deadlines/<int:course_id>", methods=['GET', 'POST'])
def deadlines(course_id):
	course = Course.query.get_or_404(int(course_id))
	display = Deadline.query.filter_by(course=course_id).all()
	return render_template("deadlines.html", display=display, course=course)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))
