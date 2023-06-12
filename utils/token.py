from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadData
from apps import configuration


class TokenHelper:
    def __init__(self) -> None:
        self._serializer = URLSafeTimedSerializer(configuration.SECURITY_PASSWORD_SALT)

    def generate_confirmation_token(self, email: str) -> tuple:
        result = None

        try:
            result = self._serializer.dumps(email, salt=configuration.SECURITY_PASSWORD_SALT)
        except (BadData, Exception) as err:
            print("Failed to generate confirmation token.")
            return False, "Failed to generate confirmation token.", None
        
        return True, None, result

    def validate_token(self, token) -> tuple:
        try:
            email = self._serializer.loads(
                token,
                salt=configuration.SECURITY_PASSWORD_SALT,
                max_age=configuration.EMAIL_TOKEN_EXPIRATION
            )
        except BadData as err:
            print("Email confirmation link is invalid or has expired")
            return False, "Email confirmation link is invalid or has expired.", None

        return True, None, email