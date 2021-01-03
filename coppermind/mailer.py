# from coppermind.main import db
# from coppermind.models import Student, Course, Signup, Deadline
import yagmail

yag = yagmail.SMTP(user='coppermind.harmony@gmail.com', password='HeroOfAges')

# class MakeMailer():
# 	def send_mail(self, student):
# 		courses = db.session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==student.id).order_by(Signup.course_id).all()
# 		contents = 'Here are your upcoming deadlines:\n\n'
# 		for course in courses:
# 			contents += course.course_name + '\n'
# 			for work in course.deadlines:
# 				contents += work.__repr__()
# 			contents += '____________________\n'

# 		try:
# 		    # yag.send(to=student.email, subject='A Message from Sazed', contents=contents)
# 		    print("Email sent successfully")
# 		except:
# 		    print("Error, email was not sent")

# 		return contents


try:
    yag.send(to="hardikti@gmail.com", subject='A Message from Sazed', contents="TEST PLEASE")
    print("Email sent successfully")
except:
    print("Error, email was not sent")