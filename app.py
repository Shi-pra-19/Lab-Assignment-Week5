from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')
        
        student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
        db.session.add(student)
        db.session.commit()

        for course_id in courses:
            enrollment = Enrollment(estudent_id=student.student_id, ecourse_id=course_id)
            db.session.add(enrollment)
            db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', student=student)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    return render_template('student.html', student=student, enrollments=enrollments)

if __name__ == '__main__':
    app.run(debug=True)
