from flask_restx import Namespace, Resource, fields
from ..models.tables import Course, User, Grade, Student, Teacher, Enrollment
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..utils import db
from ..utils.gpa import get_gpa, get_grade
from ..utils.decorators import admin_required, teacher_required
from datetime import datetime
from werkzeug.security import generate_password_hash
from ..routes.students import student_namespace

course_namespace = Namespace('Courses', description= 'Course Operations')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description='An ID'),
        'name' : fields.String(description='The name of the course'),
        'credit_hours' : fields.Integer(description='Number of credit hours'),
        'teacher' : fields.String(description= 'Name of course intructor'),
        'teacher_id' : fields.Integer(description= 'id of course intructor'),
        'created_at': fields.String(description= 'time course was created'),
        'enrollment': fields.String(description= 'Students enrolled in course')
    }
)

create_course_model = course_namespace.model(
    'CreateCourse', {
        'id': fields.Integer(description='An ID'),
        'name' : fields.String(description='The name of the course'),
        'credit_hours' : fields.Integer(description='Number of credit hours'),
        'teacher_id' : fields.Integer(description= 'Name of course intructor'),
    }
)

update_course_model = course_namespace.model(
    'UpdateCourse', {
        'name' : fields.String(description='The name of the course'),
        'teacher_id' : fields.Integer(description= 'Name of course intructor'),
    }
)

course_grading_model = course_namespace.model(
    'Grades', {
        'id': fields.Integer(description='An ID'),
        'course_id': fields.Integer(description= 'course_id'),
        'student_id': fields.Integer(description="Student ID"),
        'score': fields.Integer(description='Enter score of Student'),
        'grade': fields.Integer(description='Enter grade of Student')
    }
)

student_enrollment_model = course_namespace.model(
    'Enrollment', {
    # 'id' : fields.Integer(description= 'AN ID'),
    'student_id' : fields.Integer(description = 'student id number'),
    'course_id' : fields.Integer(description= 'course id')
    }
)
student_model = course_namespace.model(
    'Student', {
        'id': fields.String(description="Student's id"),
        'name': fields.String(description= "Student's name"),
        'email': fields.String(description="Student's Email"),
        'password_hash': fields.String(description="Student's password hash"),
        'role': fields.String(required=True, description="Role of User"),
        'courses': fields.String(description="Student's Courses")
    }
)



@course_namespace.route('/course')
class CourseGetCreate(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Get all courses",
    )
    @jwt_required()
    # get all courses
    def get(self):
        """
            Get all courses
        """
        # returns an empty list of orders
        courses = Course.query.all()

        return courses, HTTPStatus.OK


    # create a course by admin only
    @course_namespace.expect(create_course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Create a course by admin only",
    )
    # @admin_required()
    @jwt_required()
    def post(self):
        """
            Create a course
        """

        # new_course = User.query.filter_by(name=name).first()


        data = course_namespace.payload

        # checking if course already exists
        course = Course.query.filter_by(name=data['name']).first()
        if course:
            return {"message": "This course already exists"}, HTTPStatus.CONFLICT

        new_course = Course (
            name = data['name'],
            teacher_id = data['teacher_id']
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDelete(Resource):

    # getting a course
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Retreive a course by its id",
        params = {'course_id': "An ID for a course"}
    )
    @jwt_required()
    def get(self, course_id):
        """
            Retreiving a course by id
        """
        course = Course.query.filter_by(id =course_id).first()

        return course, HTTPStatus.OK

    # updating a course
    @course_namespace.expect(update_course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Updating a course by id",
        params = {'course_id': "An ID for a course"}

    )

    @admin_required() 
    def put(self, course_id):
        """
            Update a course by id by only admin
        """
        course_to_update = Course.query.filter_by(id=course_id).first()

        data = course_namespace.payload

        course_to_update.name = data["name"]
        course_to_update.teacher_id = data["teacher_id"]

        course_to_update.update()

        return course_to_update, HTTPStatus.OK


    # deleting a course
    @course_namespace.doc(
        description = "Delete a course by id",
        params = {'course_id': "An ID for a course"}

    )
    @admin_required()
    def delete(self, course_id):
        """
            Delete a course
        """

        course_to_delete = Course.query.filter_by(id=course_id).first()

        course_to_delete.delete()

        return {"message": "Course Deleted Successfully"}, HTTPStatus.OK


@course_namespace.route('/<int:course_id>/students/<int:student_id>')
class AddDropCourseStudent(Resource):
    @course_namespace.marshal_with(student_enrollment_model)
    @course_namespace.doc(
        description = "Enroll a Student for a Course",
        params = {
            'course_id': "The Course's ID"
        }
    )
    # @admin_required()
    def post(self, course_id, student_id):
        """
            Enroll a Student for a Course
        """
        course = Course.query.filter_by(id=course_id).first()
        student = Student.query.filter_by(id=student_id).first()
        
        student_in_course = Enrollment.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()
        if student_in_course:
            return {
                "message": f"{student.name} is already registered for {course.name}"
            }, HTTPStatus.OK
        
        course_student =  Enrollment(
            course_id = course_id,
            student_id = student_id
        )

        course_student.save()

        # course_student_resp = {}
        # course_student_resp['course_id'] = course_student.course_id
        # course_student_resp['course_name'] = course.name
        # course_student_resp['course_teacher'] = course.teacher
        # course_student_resp['student_id'] = course_student.student_id
        # course_student_resp['student_name'] = student.name

        return course_student, HTTPStatus.CREATED

    
@course_namespace.route('/<int:course_id>/students')
class GetAllCourseStudents(Resource):
    @course_namespace.doc(
        description = "Get all Students Enrolled for a Course",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    def get(self, course_id):
        """
            Get all Students Enrolled for a Course
        """
        get_students_in_course = Enrollment.get_students_in_course_by(course_id)
        resp = []

        for student in get_students_in_course:
            student_resp = {}
            student_resp['id'] = student.id
            student_resp['name'] = student.name

            resp.append(student_resp)

        return resp, HTTPStatus.OK


# getting all the courses a student is enrolled in
@course_namespace.route('/student/<int:student_id>/courses')
class StudentCourses(Resource):
    # @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Get a student's courses by student id",
        params = {'student_id': "An ID for a student"}
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all student's courses
        """
        courses = []
        student = Student.query.filter_by(id=student_id).first()

        student_courses = student.courses
        

        for course in student_courses:
        #     # return course
            course_resp = {}
            # course_resp['course_name'] = course.name
            course_resp['course_id'] = course.id

            courses.append(course_resp)

        return courses, HTTPStatus.OK