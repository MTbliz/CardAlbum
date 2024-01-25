from src.models import User


class UserRepository:

    def get_possible_customers(self, user_id: int) -> list[User]:
        possible_customers: list[User] = User.query.filter(User.id != user_id).all()
        return possible_customers

    def get_user_by_email(self, email: str) -> User:
        user: User = User.query.filter_by(email=email).first()
        return user
