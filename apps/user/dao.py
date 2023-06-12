from sqlalchemy.exc import SQLAlchemyError
from apps import db
from apps.user.models import User
from utils.blog_logger import BlogLogger


class UserDao:
    @staticmethod
    def create_user(
                    username: str,
                    email: str,
                    password: str,
                ):
        
        user = User(username, email, password)

        with db.session.begin():
            try:
                db.session.add(user)
            except SQLAlchemyError as err:
                BlogLogger.get_instance().log_error(f"Failed to add user data into database. {str(err)}.")
                return False, "Failed to update database.", None
                  
        return True, None, user

    def get_user_by_email(
            email: str,
            ) -> tuple:
        result = None

        BlogLogger.get_instance().log_info(f"Getting user with email {email} from database.")

        with db.session.begin():
            try:
                result = User.query.filter_by(email=email).first()
            except SQLAlchemyError as err:
                BlogLogger.log_error(f"Failed to search user by email in database. {str(err)}.")
                return False, "Failed to read data from database.", None
            
        return True, None, result
    
    def get_user_by_id(
            id: int,
            ) -> tuple:
        result = None

        BlogLogger.get_instance().log_info(f"Getting user with id {id} from database.")

        with db.session.begin():
            try:
                result = User.query.get(id)
            except SQLAlchemyError as err:
                BlogLogger.log_error(f"Failed to search user by id in database. {str(err)}.")
                return False, "Failed to read data from database.", None
            
        return True, None, result