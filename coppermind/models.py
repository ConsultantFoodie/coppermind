from coppermind.main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	gender = db.Column(db.Integer, nullable=False)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	courses = db.relationship('Course', secondary='signup')

	def __repr__(self):
		return '{}, {}, {}, {}, {}, {}\n'.format(self.id, self.gender, self.username, self.email, self.password, self.courses)

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_name = db.Column(db.String(150), unique=True, nullable=False)
	deadlines = db.relationship('Deadline', backref='course_in', lazy=True, cascade="all, delete, delete-orphan")
	students = db.relationship('Student', secondary='signup')

	def __repr__(self):
		return '{}: {}\n'.format(self.course_name, self.deadlines)

class Signup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False) #This is course.id
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

	def __repr__(self):
		return 'C:{}, S:{}\n'.format(self.course_id, self.student_id)

class Deadline(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	work_type = db.Column(db.Integer, nullable=False)
	brief_desc = db.Column(db.String(100), nullable=False)
	details = db.Column(db.String(750))
	course = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
	submit_date = db.Column(db.Date, nullable=False)
	submit_time = db.Column(db.Time, nullable=False)

	def __repr__(self):
		work_list = ['Other', 'Quiz', 'Test', 'Submission', 'Project', 'Viva']
		deadline_str = "\n{0}\nDate: {1}\nTime: {2}\nBrief Details: {3}\n".format(work_list[int(self.work_type)], self.submit_date.strftime("%d %b, %Y. %A"),
																			self.submit_time.strftime("%H:%M"), self.brief_desc)
		return deadline_str
# class HasWork(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False) #This is course.id
# 	deadline_id = db.Column(db.Integer, db.ForeignKey('deadline.id'), nullable=False)

# 	def __repr__(self):
# 		return 'C:{}, D:{}\n'.format(self.course_id, self.deadline_id)