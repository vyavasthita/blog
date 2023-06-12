from dataclasses import dataclass
from utils.http_status import HttpStatus


@dataclass
class Response:
    status: HttpStatus
    message: str