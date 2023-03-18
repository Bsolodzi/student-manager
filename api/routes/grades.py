from flask_restx import Namespace, Resource, fields, abort, marshal
from api.models.tables import User, Admin, Teacher, Grade, Enrollment, Course, Student
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from ..utils import db
from sqlalchemy import exc
from ..utils.gpa import get_gpa, get_grade

grading_namespace = Namespace('Grades', description= 'namespace for grades')

grade_model = grading_namespace.model(
    'Grade', {
    'id' : fields.Integer(description="Grade ID"),
    'student_id' : fields.Integer(description= "ID of student to to score"),
    'course_id' : fields.Integer(description="ID of the course"),
    'score': fields.Integer(description="Score of student in course"),
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

@grading_namespace.route('/grades/student/<int:student_id>')
class CourseGrades(Resource):
    @grading_namespace.expect(course_grading_model)
    # since we are returning use marshall
    @grading_namespace.marshal_with(grade_model)
    @grading_namespace.doc(
        description = "Grade a student in course by course id",
        # params = {'course_id': "An ID for a courses"}
    )
    @jwt_required()
    # @teacher_required()
    def put(self, student_id):
        """
            Grade a student in a course
        """
        # user_allowed = get_jwt_identity()
        # author_admin = Admin.query.filter_by(email=user_allowed).first()
        # author_student = Student.query.filter_by(email= user_allowed).first()

        # data = grading_namespace.payload

        # user_id = Student.query.filter_by(id = student_id).first()
        # user_id_id = user_id.id
        # grades = Grade.query.filter_by(student=user_id_id).all()
        # try:
        #     if len(grades) >= 1:
        #         return {'message': "You are not authorized to grade this student again"}, HTTPStatus.UNAUTHORIZED
        #     else:
        #         if author_admin:
        #             set_grade = Grade(score= data['score'])
        #             set_grade.student = user_id_id
        #             print (set_grade.student)
        #             set_grade.save()
        #             return set_grade, HTTPStatus.CREATED
        #         elif author_student:
        #             return {'message': "You are unauthorized"}, HTTPStatus.UNAUTHORIZED
        # except AttributeError:
        #     return {'message': 'User not found'}

        # data = grading_namespace.payload
        # data = student_namespace.payload
        # student = Student.query.filter_by(id=student_id).first()
        # course = Course.query.filter_by(id=data['course_id'])
        
        # # Confirm that the student is taking the course
        # student_course = Enrollment.query.filter_by(student_id=student_id, course_id=course.id).first()
        # if not student_course:
        #     return {"message": f"{student.name}] is not taking {course.name}"}, HTTPStatus.NOT_FOUND
        
        # # Add a new grade
        # new_grade = Grade(
        #     student_id = student_id,
        #     course_id = data['course_id'],
        #     score = data['score'],
        #     grade = get_grade(data['score'])
        # )

        # new_grade.save()

        # grade_resp = {}
        # grade_resp['grade_id'] = new_grade.id
        # grade_resp['student_id'] = new_grade.student_id
        # grade_resp['student_name'] = student.name
        # grade_resp['course_id'] = new_grade.course_id
        # grade_resp['course_name'] = course.name
        # grade_resp['course_teacher'] = course.teacher
        # grade_resp['score'] = new_grade.score
        # grade_resp['gpa'] = new_grade.letter_grade

        # return grade_resp, HTTPStatus.CREATED

# @grading_namespace.route('/grades')
# class GetPostGrades(Resource):
#     @grading_namespace.expect(grade_model)
#     @grading_namespace.marshal_with(grade_model)
#     @grading_namespace.doc(
#         description = "Score a student"
#     )
#     # @jwt_required()
#     def post (self):

#         data = grading_namespace.payload
#         # student = Student.get_id_by(student_id)

#         #  = Enrollment.query.filter_by(id = enrollment_id).first()

#         new_grade = Grade (
#             # name = data['name'],
#             # teacher_id = data['teacher_id']
#             student_id = data['student_id'],
#             course_id = data['course_id'],
#             score = data['score'],
#             grade = get_grade('score'),
#             gpa= get_gpa(data['grade'])
#         )

#         new_grade.save()

#         return new_grade, HTTPStatus.CREATED





    # def post(self, student_id, course_id):
    #     """
    #         post a new grade
    #     """

    #     data = grading_namespace.payload
    #     score = data['score']

    #     course = Course.query.filter_by(id = course_id).first()
    #     student = Student.query.filter_by(id = student_id).first()

    #     course_teacher = course.teacher
    #     current_user = get_current_user

    #     if course_teacher != current_user:
    #         abort(403, message= "only course teacher can grade student")
    #     error_msg = None

    #     if student not in course.students:
    #         error_msg = "This student did is not enrolled for this course"
        
    #     try:
    #         grade = Grade(student_id = student_id, course_id = course_id, score = score)
    #         grade.get_grade()
    #         grade.save()
    #         return marshal(grade, grade_model), HTTPStatus.CREATED
    #     except exc.IntegrityError:
    #         error_msg = 'This student did not register for this course'

    #     abort(400, message= error_msg)
        # new_grade = Grade(
        #     # student_id = data['student_id'],
        #     student_id = data[student_id],
        #     # course_id = data['course_id'],
        #     score = data['score'],
        #     gpa = data['gpa']

        # )

        # new_grade.save()
        # db.session.add(new_grade)
        # db.session.commit()

        # return new_grade, HTTPStatus.OK


        
