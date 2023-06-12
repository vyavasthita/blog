from functools import wraps
from werkzeug.security import check_password_hash
from apps.user.dao import UserDao
from utils.http_status import HttpStatus


def validate_registration(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper

def validate_unique_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_success, message, user = UserDao.get_user_by_email(email=args[2])
        
        if not is_success:
            return False, message, None
        
        if user is not None:
            return False, "User already exists", None
        
        return func(*args, **kwargs)
    
    return wrapper

def check_user_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_success, message, user = UserDao.get_user_by_email(email=args[1])
        
        if not is_success:
            return False, message, None        
        elif user is None:
            return False, "User with email '{}' does not exist.".format(args[1]), None
        else:
            if not check_password_hash(user.password, args[2]):
                return False, "Invalid Password.", None

        return True, None, user
    
    return wrapper