from flask import abort
from flask_login import current_user
from loguru import logger

from src.models import User
from src.user.user_repository import UserRepository


class UserService:

    def __init__(self) -> None:
        self.user_repository: UserRepository = UserRepository()

    def get_possible_customers(self, user_id: int) -> list[User]:
        logger.info(f"Fetching possible customers for user with ID {user_id}")
        if current_user.id != user_id:
            logger.warning(
                f"Access denied: Current user {current_user.id} does not match the requested user ID {user_id}")
            abort(403)
        else:
            customers = self.user_repository.get_possible_customers(user_id)
            logger.info(f"Found customers possible customers for user with ID {user_id}")
            return customers

    def get_user_by_email(self, email: str) -> User:
        logger.info(f"Looking up user by email: {email}")
        user = self.user_repository.get_user_by_email(email)
        if user:
            logger.info(f"User with email {email} found: {user.username}")
        else:
            logger.warning(f"No user found with email: {email}")
        return user
