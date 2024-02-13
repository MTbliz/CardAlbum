from flask import abort
from flask_login import current_user
from loguru import logger

from src.models import User, Invite
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

    def get_user_contacts(self, user_id: int, page: int, ROWS_PER_PAGE: int) -> list[User]:
        contacts = self.user_repository.get_user_contacts(user_id, page, ROWS_PER_PAGE)
        return contacts

    def get_user_invites(self, user_id: int) -> list[User]:
        invites = self.user_repository.get_user_invites(user_id)
        return invites

    def send_invite(self, user_id: int, user_email: str) -> bool:
        user = self.user_repository.get_user_by_email(user_email)
        if user:
            self.user_repository.send_invite(user_id, user_email)
            return True
        else:
            return False

    def delete_invite(self, invite_id: int) -> None:
        logger.info(f"Attempting to delete invite with ID {invite_id}.")
        invite: Invite = self.user_repository.get_invite(invite_id)
        if invite is None:
            logger.error(f"Invite with ID {invite_id} not found.")
            abort(404)
        elif current_user.id != invite.contact_id:
            logger.warning(f"User {current_user.id} tried to delete invite {invite_id} owned by another user.")
            abort(403)
        else:
            self.user_repository.delete_invite(invite_id)
            logger.info(f"Successfully deleted invite with ID {invite_id}.")

    def add_contact(self, invite_id) -> None:
        logger.info(f"Attempting to add contact using invite with ID: {invite_id}.")
        invite: Invite = self.user_repository.get_invite(invite_id)
        if current_user.id != invite.contact_id:
            logger.warning(f"User {current_user.id} tried to add contact {invite.user_id} owned by another user.")
            abort(403)
        else:
            logger.info(f"User {current_user.id} add contact {invite.user_id}.")
            self.user_repository.add_contact(invite)
