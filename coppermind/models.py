from coppermind.main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	gender = db.Column(db.Integer, nullable=False)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(40), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	courses = db.relationship('Course', secondary='signup')

	def __repr__(self):
		return '{}, {}, {}, {}, {}, {}\n'.format(self.id, self.gender, self.username, self.email, self.password, self.courses)


# DO NOT CONFUSE BETWEEN course.id and course.course_id. Plan to change var name
class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.String(7), unique=True, nullable=False)
	deadlines = db.Column(db.String(100), nullable=True)
	students = db.relationship('Student', secondary='signup')

	def __repr__(self):
		return '{}'.format(self.course_id, self.deadlines)

class Signup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

	def __repr__(self):
		return 'C:{}, S:{}\n'.format(self.course_id, self.student_id)