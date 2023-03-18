from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_current_user
from functools import wraps
from http import HTTPStatus
from ..models.tables import User,Student, Teacher


# get the user role
def get_user_role(id:int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.role 
    return None

# decorator to handle admin authorization
def admin_required():
    """
    Decorator to allow only users with `ADMIN` role access
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator (*args,**kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if get_user_role(claims['sub']) == 'admin':
                return fn (*args, **kwargs)
            return {'message':"Administrator access required"}, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper


# decorator to handle teacher authorization
def teacher_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_role(claims['sub']) == 'teacher':
                return fn(*args, **kwargs)
            return {"message": "Teacher access only"}, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper

def student_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_role(claims['sub']) == 'student':
                return fn(*args, **kwargs)
            return {"message": "Student access only"}, HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper

