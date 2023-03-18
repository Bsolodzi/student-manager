from ..utils import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique =True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    role = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)

    def __repr__(self):
        return self.email    
    

class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key= True)
    # courses = db.relationship('Course', backref ='admin', lazy = True)

    __mapper_args__ = {
        'polymorphic_identity': "admin"
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Teacher(User):
    __tablename__ = "teacher"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key= True)
    courses = db.relationship('Course', backref= 'teacher', lazy = True)

    __mapper_args__ = {
        'polymorphic_identity':  'teacher'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)

    def __repr__(self):
        return self.email 

class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key= True)
    courses = db.relationship('Enrollment', backref= 'student', lazy = True)

    __mapper_args__ = {
        'polymorphic_identity':  'student'
    }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)

    def __repr__(self):
        return self.email 

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), nullable=False)
    credit_hours = db.Column(db.Integer, default = 1)
    # admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    enrollments = db.relationship('Enrollment', backref= 'course', lazy = True)
    created_at = db.Column(db.DateTime(), nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return f'Course {self.id}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)

    def __repr__(self):
        return self.email 
    
class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key= True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade = db.relationship('Grade', backref ='enrollment', lazy = True)

    def __repr__(self):
        return f'Enrollment {self.id}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)
    
    @classmethod
    def get_students_in_course_by(cls, course_id):
        students = Student.query.join(Enrollment).join(Course).filter(Course.id == course_id).all()
        return students

    @classmethod
    def get_student_courses(cls, student_id):
        courses = Course.query.join(Enrollment).join(Student).filter(Student.id == student_id).all()
        return courses
    


class Grade (db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    score = db.Column(db.Float, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'))

    def __repr__(self):
        return f'Grade {self.student.name} {self.course.name} {self.value}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_id_by(cls, id):
        return cls.query.get_0r_404(id)

    def __repr__(self):
        return self.email 