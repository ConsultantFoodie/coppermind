# Coppermind

## The deadline reminder

Using coppermind, students will be able to add deadline reminders for courses they are registered in, and a daily email will be sent to each student for all upcoming reminders. Only one student will need to add a reminder for a course and every one registered for that course will receive a mail.

Quick Instructions to set it up locally.
1. Install postgres and create a database. Set an environment variable DATABASE_URL as the location of the database(postgres:///{name})
2. Clone repo and install the requirements in a virtual environment.
3. For working with Flask-Migrate, set another environment variable FLASK_APP=run.py
4. Execute run.py and access localhost:5000. The site should be running.
