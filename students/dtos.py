from dataclasses import dataclass

from users.models import User


@dataclass
class StudentsPaginationDto:
    entities: list[User]
    total: int
