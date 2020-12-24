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
	courses = db.Column(db.String(100), nullable=True)

	def __repr__(self):
		return '{}, {}, {}, {}, {}, {} \n'.format(self.id, self.gender, self.username, self.email, self.password, self.courses)