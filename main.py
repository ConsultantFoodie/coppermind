from flask import Flask, render_template, url_for, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'IAmTheHeroOfAges'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
db = SQLAlchemy(app)

class Student(db.Model):
	email = db.Column(db.String, primary_key=True)
	courses = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return '{}: {}'.format(self.email, self.courses)


@app.route('/', methods=['GET', 'POST'])
def index():
	reg_form = RegistrationForm()
	if reg_form.validate_on_submit():
		print(Student.query.all())
		try:
			existing = Student.query.get_or_404(reg_form.email.data)
		except:
			if reg_form.take_or_drop.data == '1':
				student = Student(email=reg_form.email.data, courses=reg_form.course_id.data+';')
				try:
					db.session.add(student)
					db.session.commit()
				except:
					return "ERROR: Cannot register"

		

	return render_template("index.html", reg_form=reg_form)

if __name__ == "__main__":
	app.run(debug=True)