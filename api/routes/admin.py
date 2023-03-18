from ..models.tables import Admin, User
from flask_restx import Namespace, fields, Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from ..utils import db
from ..utils.decorators import admin_required
from datetime import datetime
from werkzeug.security import generate_password_hash

admin_namespace = Namespace('admin', description= 'Admin Operations')

admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'name': fields.String(required=True, description="Admin's Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin's User ID"),
        'name': fields.String(required=True, description="Admin's Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password_hash': fields.String(required=True, description="Admin's Password"),
        'role': fields.String(required=True, description="Role of User")
    }
)
    
@admin_namespace.route('/register')
class AdminRegistration(Resource):

    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.marshal_with(admin_model)
    # Uncomment the @admin_required() decorator below after creating the super admin(proprietor in this logic)
    # This will then mean that only the proprietor can create an admin account and handover the system to him 
    # @admin_required()
    @admin_namespace.doc(
        description = "Register an Admin by porprietor or subsequent admins"
    )
    def post(self):
        """
            Register an Admin. this can only be used after the createion of the first super admin(first admin) 
        """        
        data = admin_namespace.payload

        # Register new admin
        new_admin = Admin(
            name = data['name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            role = 'admin'
        )

        new_admin.save()

        return new_admin, HTTPStatus.CREATED
    
@admin_namespace.route('')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Get All Admins by only admins"
    )
    @admin_required()
    def get(self):
        """
            Get All Admins - Admins Only
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK