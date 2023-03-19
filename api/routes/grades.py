from flask_restx import Namespace, Resource, fields, abort, marshal
from api.models.tables import User, Admin, Teacher, Grade, Enrollment, Course, Student
from http import HTTPStatus
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, get_current_user, get_jwt
from ..utils import db
from ..utils.decorators import teacher_required, admin_required, get_user_role
from sqlalchemy import exc
from ..utils.gpa import get_gpa, get_grade

grading_namespace = Namespace('Grades', description= 'Grades operations')

grade_model = grading_namespace.model(
    'Grade', {
    'id' : fields.Integer(description="Grade ID"),
    'student_id' : fields.Integer(description= "ID of student to to score"),
    'course_id' : fields.Integer(description="ID of the course"),
    'score': fields.Integer(description="Score of student in course"),
    'grade': fields.String(description= 'grade of student'),
    'gpa': fields.Integer(description='gpa of course')
    }
)

course_grading_model = grading_namespace.model(
    'Grade', {
        'student_id' : fields.Integer(description= "ID of student to to score"),
        'course_id' : fields.Integer(description="ID of the course"),
        'score': fields.Integer(required = True, description= "Student's score in course")
    }
)

# Verify student or admin access
def is_student_or_admin(student_id:int) -> bool:
    claims = get_jwt()
    active_user = get_jwt_identity()
    if (get_user_role(claims['sub']) == 'admin') or (active_user == student_id):
        return True
    else:
        return False

@grading_namespace.route('/grades/student/<int:student_id>')
class CourseGrades(Resource):
    @grading_namespace.expect(course_grading_model)
    # since we are returning use marshall
    # @grading_namespace.marshal_with(grade_model)
    @grading_namespace.doc(
        description = "Grade a student in course by course id",
        # params = {'course_id': "An ID for a courses"}
    )
    # @admin_required()  
    def put(self, student_id):
        """
            Grade a student in a course
        """

        data = grading_namespace.payload

        student = Student.query.filter_by(id=data['student_id']).first()
        course = Course.query.filter_by(id=data['course_id']).first()
        
        # Confirm that the student is taking the course
        student_course = Enrollment.query.filter_by(student_id=student.id, course_id= course.id).first()
        already_graded = Grade.query.filter_by(student_id=student.id, course_id= course.id).first()
        if not student_course:
            return {"message": f"{student.name} is not taking {course.name}"}, HTTPStatus.NOT_FOUND
        elif already_graded:
            return {"message": f"{student.name} is already graded for {course.name}"}, HTTPStatus.NOT_FOUND
        
        # Add a new grade
        new_grade = Grade(
            student_id = data['student_id'],
            course_id = data['course_id'],
            score = data['score'],
            grade = get_grade(data['score']),
        )

        new_grade.save()

        # return new_grade, HTTPStatus.CREATED

        grade_resp = {}
        grade_resp['grade_id'] = new_grade.id
        grade_resp['student_id'] = new_grade.student_id
        grade_resp['student_name'] = student.name
        grade_resp['course_id'] = new_grade.course_id
        grade_resp['course_name'] = course.name
        grade_resp['course_teacher_id'] = course.teacher_id
        grade_resp['score'] = new_grade.score
        grade_resp['grade'] = new_grade.grade
        grade_resp['gpa'] = get_gpa(grade_resp['grade'])

        return grade_resp, HTTPStatus.CREATED

# route for getting and deleting grades
@grading_namespace.route('/grade/<int:grade_id>')
class GetUpdateDelete(Resource):

    # getting a grade for
    @grading_namespace.marshal_with(grade_model)
    @grading_namespace.doc(
        description = "Retreive a grade by its id",
        params = {'grade_id': "An ID for a grade"}
    )
    @jwt_required()
    def get(self, grade_id):
        """
            Retreiving a grade by id
        """
        grade = Grade.query.filter_by(id =grade_id).first()

        return grade, HTTPStatus.OK

# deleting a grade from the system
    @admin_required()
    def delete(self, grade_id):
        """
            Delete a grade
        """
        grade_to_delete = Grade.query.filter_by(id=grade_id).first()

        grade_to_delete.delete()

        return {"message": "Grade Deleted Successfully"}, HTTPStatus.OK
    

@grading_namespace.route('/<int:student_id>/cgpa')
class GetStudentCGPA(Resource):

    @grading_namespace.doc(
        description = "Calculate a Student's CGPA",
        params = {
            'student_id': "The Student's ID"
        }
    )
    # @admin_required()
    @jwt_required()
    def get(self, student_id):
        """
            Calculate a Student's CGPA 
        """
        current_user = User.query.filter_by(id=student_id).first()
        
        # if is_student_or_admin(student_id):
        if current_user.id == student_id or current_user.role == "admin" or current_user.role == 'teacher':

            student = Student.query.filter_by(id = student_id).first()
                
            courses = Enrollment.query.filter_by(id = student_id).all()
                
            total_gpa = 0
                
            for course in courses:
                grades = Grade.query.filter_by(
                        student_id=student_id 
                        ).all()
                
                if grades:
                    
                    for grade in grades:

                        grade = grade.grade
                        gpa = get_gpa(grade)
                        total_gpa = total_gpa + gpa
                    
                    no_of_courses = len(grades)
                else:
                    return {"message": f"{student.name} is has no grade"}, HTTPStatus.OK
                
            cgpa = total_gpa / no_of_courses
            round_cgpa = float("{:.3f}".format(cgpa))

            return {"message": f"{student.name}'s CGPA is {round_cgpa} with total GPA: {total_gpa}"}, HTTPStatus.OK
        
        else:
            return {"message": "Admins or Specific Student Only"}, HTTPStatus.FORBIDDEN