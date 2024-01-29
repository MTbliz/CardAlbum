from flask import abort
from flask_login import current_user

from src.models import User
from src.user.user_repository import UserRepository


class UserService:

    def __init__(self) -> None:
        self.user_repository: UserRepository = UserRepository()

    def get_possible_customers(self, user_id: int) -> list[User]:
        if current_user.id != user_id:
            abort(403)
        else:
            return self.user_repository.get_possible_customers(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)
