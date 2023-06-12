import random
import string


class PasswordGenerator:
    def __init__(self, length: int) -> None:
        self._length = length
        self._lower = string.ascii_lowercase
        self._upper = string.ascii_uppercase
        self._num = string.digits
        self._symbols = string.punctuation

    def generate_password(self) -> str:
        password = None

        try:
            all = self._lower + self._upper + self._num + self._symbols
            password = "".join(random.sample(all, self._length))
        except Exception as err:
            return False, "Failed to generate password. {}".format(str(err)), None

        return True, None, password