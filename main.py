from flask import Flask, render_template, url_for, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

'''
	TODO: Add passwords for users so that emails are not misused
		  Add course details section
		  Use CSS if possible
'''

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
		reg_form.course_id.data = reg_form.course_id.data.upper()
		try:
			existing = Student.query.get_or_404(reg_form.email.data)
			#If student exists, adding or dropping courses according to their choice
			course_list = existing.courses.split(';')
			if reg_form.take_or_drop.data == '1':
				if reg_form.course_id.data not in course_list:
					course_list.append(reg_form.course_id.data)
			else:
				if reg_form.course_id.data in course_list:
					course_list.remove(reg_form.course_id.data)
			try:
				if len(course_list) == 0:
					db.session.delete(existing)
				else:
					existing.courses = ';'.join(course_list)
				db.session.commit()
			except Exception as e:
				return "ERROR: Cannot process request\n\n{}".format(e)

			return redirect(url_for('index'))
		except:
			# Adding student in database if registering for a course
			# Ignoring if dropping a course since student does not exist in database
			if reg_form.take_or_drop.data == '1':
				student = Student(email=reg_form.email.data, courses=reg_form.course_id.data)
				try:
					db.session.add(student)
					db.session.commit()
				except Exception as e:
					return "ERROR: Cannot process request\n\n{}".format(e)
			return redirect(url_for('index'))
		
	print(Student.query.all())
	return render_template("index.html", reg_form=reg_form)

if __name__ == "__main__":
	app.run(debug=True)