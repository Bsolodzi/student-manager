from flask_restx import Namespace, Resource, fields, marshal
from ..models.tables import Course, User,Admin, Grade, Student, Teacher, Enrollment
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..utils import db
from ..utils.decorators import admin_required, teacher_required
from datetime import datetime
from werkzeug.security import generate_password_hash

teacher_namespace = Namespace('Teacher', description= 'Teacher Operations')

teacher_model = teacher_namespace.model(
    'Teacher', {
        'id': fields.String(description="Student's id"),
        'name': fields.String(description= "Student's name"),
        'email': fields.String(description="Student's Email"),
        'password_hash': fields.String(description="Student's password hash"),
        'role': fields.String(required=True, description="Role of User"),
        'courses': fields.String(description="Student's Courses")
    }
)

teacher_signup_model = teacher_namespace.model(
    'TeacherSignup', {
        'name': fields.String(required=True, description="Student's Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, description="Student's Password"),
    }
)

@teacher_namespace.route('/teachers')
class GetAllTeachers(Resource):
    # @teacher_namespace.expect(teacher_signup_model)
    # @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(
        description = "Get all Teachers",
    )
    
    # is_student= Student.query.filter_by(role=current_user).first()

    # @jwt_required()
    # @admin_required()
    def get(self):
        """
        Get all teachers
        # """
        # current_user = get_jwt_identity()
        # is_admin = Admin.query.filter_by(role= current_user).first()
        # if is_admin:
        #     teachers = Teacher.query.all() 
        #     return teachers, HTTPStatus.OK
        # return {'message': "You are unauthorized"}, HTTPStatus.UNAUTHORIZED
        teachers = Teacher.query.all()

        return marshal(teachers, teacher_model), HTTPStatus.OK

@teacher_namespace.route('/register')
class SignUpTeacher(Resource):
    @teacher_namespace.expect(teacher_signup_model)
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(
        description = "Create a Teacher Account",
    )
    # @admin_required()
    # @jwt_required()
    def post(self):
        """
            Create a Teacher account
        """
        # verify_jwt_in_request()

        # current_user = User.query.filter_by().first()
        
        # checks if a the user is either the admin
        # if current_user.role == "admin":

        data = teacher_namespace.payload

        new_teacher = Teacher (
            name = data['name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            role = 'teacher'
        )

        new_teacher.save()

        return new_teacher, HTTPStatus.CREATED
        
        # else:
            # return {"message": "You must be an Admin to create a teacher"}, HTTPStatus.FORBIDDEN