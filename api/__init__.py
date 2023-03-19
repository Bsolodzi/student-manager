from flask import Flask
from flask_restx import Api
from api.config.config import config_dict
from api.utils import db
from api.models.tables import Course, User, Admin, Grade, Student, Teacher, Enrollment
from .auth.views import auth_namespace
from .routes.courses import course_namespace
from .routes.teachers import teacher_namespace
from .routes.grades import grading_namespace
from .routes.students import student_namespace
from .routes.admin import admin_namespace

from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    #telling db, this is our app
    db.init_app(app)

    
    jwt = JWTManager(app)
    
    #takes two 
    # migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type" : "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt: JWT&gt token to authorize ** as prefix"
        }
    }

    api = Api(app, 
              title = "Student Management API",
              description= "A simple student management tool",
              authorizations= authorizations, 
              security= "Bearer Auth"
            )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(student_namespace, path="/student")
    api.add_namespace(course_namespace, path="/course")
    api.add_namespace(grading_namespace, path="/grade")
    api.add_namespace(teacher_namespace, path="/teacher")


    # error handling
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404 
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404

    # adding/connecting to the shell so that we can migrate and create the db
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            "Users": User,
            "Admin": Admin,
            'Teacher': Teacher,
            "Student": Student,
            'Courses': Course,
            "Enrollment": Enrollment,
            "Grade": Grade                   
        }

    return app