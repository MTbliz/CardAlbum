from src.models import User
from src.user.user_repository import UserRepository


class UserService:

    def __init__(self) -> None:
        self.user_repository: UserRepository = UserRepository()

    def get_possible_customers(self, user_id: int) -> list[User]:
        return self.user_repository.get_possible_customers(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)
