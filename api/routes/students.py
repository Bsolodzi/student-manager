from ..models.tables import Student, Teacher, Grade, User
from flask_restx import Namespace, fields, Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from ..utils import db
from ..utils.decorators import admin_required, teacher_required
from datetime import datetime
from werkzeug.security import generate_password_hash

student_namespace = Namespace("student", description="Student Operations")

student_model = student_namespace.model(
    'Student', {
        'id': fields.String(description="Student's id"),
        'name': fields.String(description= "Student's name"),
        'email': fields.String(description="Student's Email"),
        'password_hash': fields.String(description="Student's password hash"),
        'role': fields.String(required=True, description="Role of User"),
        'courses': fields.String(description="Student's Courses")
    }
)

student_signup_model = student_namespace.model(
    'StudentSignup', {
        'name': fields.String(required=True, description="Student's Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, description="Student's Password"),
    }
)

student_enrollment_model = student_namespace.model(
    'Enrollment', {
        # 'id' : fields.Integer(description= 'AN ID'),
        'student_id' : fields.Integer(description = 'student id number'),
        'course_id' : fields.Integer(description= 'course id')
    }
)

delete_student_model = student_namespace.model(
    'DeleteStudent', {
        'student_id': fields.Integer(description='Student ID of student to less'),
    }
)

# route for creating new students
@student_namespace.route('/register')
class StudentRegisteration(Resource):
    @student_namespace.expect(student_signup_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Create a Student Account",
    )
    def post(self):
        """
            Create a student
        """
        data = student_namespace.payload

        new_student = Student (
            name = data['name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            role = 'student'
        )
        new_student.save()

        return new_student, HTTPStatus.CREATED

@student_namespace.route('/')
class GetAllStudents(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Get all students by Teachers and Admins only",
    )
    # @jwt_required()
    # @admin_required()
    # get all students in school
    def get(self):
        """
            Get all students by Teachers and Admins only
        """
        students = Student.query.all()

        return students, HTTPStatus.OK

@student_namespace.route('<int:student_id>')
class GetUpdateDeleteStudent(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Get all students by Teachers and Admins only",
        params = {'student_id': "An ID for student to be viewed"}
    )
    # @jwt_required()
    # viewing a single student details
    def get(self, student_id):
        """
            View a student's details
            
        """
        current_user = User.query.filter_by(id=student_id).first()
        
        # checks if a the user is either the admin or a teacher or the particular student(self)
        if current_user.id == student_id or current_user.role == "admin" or current_user.role == 'teacher':

            student_to_view = Student.query.filter_by(id=student_id).first()

            return student_to_view, HTTPStatus.OK
        else:
            return {"message": "You must be an Admin or the Specific Student to view this details"}, HTTPStatus.FORBIDDEN


    @student_namespace.expect(delete_student_model)
    @student_namespace.doc(
        description = "Delete a student by id",
        params = {'student_id': "An ID for student to be deleted"}
    )
    @admin_required()
    # deleting a student from the school
    def delete(self, student_id):
        """
            Delete a student from the system
        """
        verify_jwt_in_request()

        student_to_delete = Student.get_id_by(student_id)

        student_to_delete.delete()

        return {"message": "Student Deleted Successfully"}, HTTPStatus.OK
    
    @student_namespace.expect(student_signup_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Update a Student's Details by ID - Admins or Specific Student Only",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update a Student by self or admin
        """
        current_user = User.query.filter_by(id=student_id).first()

        if current_user.id == student_id or current_user.role == "admin":
        
            student = Student.query.filter_by(id=student_id).first()
                
            data = student_namespace.payload

            student.name = data['name']
            student.email = data['email']
            student.password_hash = generate_password_hash(data['password'])

            student.update()

            return student, HTTPStatus.OK
        
        else:
            return {'message': "Admin or Particular student only can make changes to this student"}