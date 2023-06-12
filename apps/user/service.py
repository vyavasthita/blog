from werkzeug.security import generate_password_hash, check_password_hash
from apps.user.dao import UserDao
from apps.user.data_validation import validate_registration, validate_unique_user, check_user_exists
from apps import configuration
from utils.password_helper import PasswordGenerator
from utils.blog_logger import BlogLogger
from utils.http_status import HttpStatus


class UserService:
    @validate_unique_user
    def sign_up(
            self,
            username: str,
            email: str
        ):
        password_generator = PasswordGenerator(configuration.PASSWORD_LENGTH)

        is_success, message, password = password_generator.generate_password()

        BlogLogger.get_instance().log_info(f"Creating user with username {username} and email {email}, {password}.")
        is_success, message, user = UserDao.create_user(username, email, generate_password_hash(password))

        if not is_success:
            return False, message, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
        
        return True, None, password

    @check_user_exists
    def sign_in(
            self,
            email,
            password,
        ):

        BlogLogger.get_instance().log_info(f"Logging user with username {email}.")
    
    def load_user(self, id: int):
        BlogLogger.get_instance().log_info(f"Loading user with id {id} .")
        is_success, message, user = UserDao.get_user_by_id(id=int(id))

        if not is_success:
            return False, message, HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
        
        return True, None, user
        
user_service = UserService()