from flask import abort
from flask_login import current_user
from loguru import logger

from src.album.album_repository import AlbumRepository
from src.card.user_card_repository import UserCardRepository
from src.models import UserCard, Album


class UserCardService:

    def __init__(self) -> None:
        self.user_card_repository: UserCardRepository = UserCardRepository()
        self.album_reposiotry: AlbumRepository = AlbumRepository()

    def get_cards(self, user_id: int, field_sort: str, order: str, filters: dict[str, str], page: int,
                  ROWS_PER_PAGE: int):
        logger.info("Retrieving all uesr_cards.")
        cards = self.user_card_repository.get_cards(user_id, field_sort, order, filters, page, ROWS_PER_PAGE)
        logger.info(f"Retrieved user_cards for user id: {user_id}")
        return cards

    def get_card(self, card_id: int) -> UserCard:
        logger.info(f"Attempting to retrieve user_card with ID {card_id}.")
        user_card = self.user_card_repository.get_card(card_id)
        if not user_card:
            logger.error(f"User_card with ID {card_id} not found.")
            abort(404)
        elif current_user.id != user_card.user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card_id} owned by another user.")
            abort(403)
        else:
            logger.info(f"User {current_user.id} accessed user_card {card_id}.")
            return user_card

    def add_card(self, card: UserCard) -> None:
        logger.info(f"Attempting to add user_card with ID {card.id}.")
        if current_user.id != card.user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card.id} owned by another user.")
            abort(403)
        else:
            self.user_card_repository.add_card(card)
            logger.info(f"User {current_user.id} add user_card {card.id}.")

    def delete_card(self, card_id: int) -> None:
        logger.info(f"Attempting to delete user_card with ID {card_id}.")
        card: UserCard = self.user_card_repository.get_card(card_id)
        if card is None:
            logger.error(f"User_card with ID {card_id} not found.")
            abort(404)
        elif current_user.id != card.user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card.id} owned by another user.")
            abort(403)
        else:
            self.user_card_repository.delete_card(card_id)
            logger.info(f"Successfully deleted user_card with ID {card_id}.")

    def check_if_user_card_exists(self, card_id: int, user_id: int) -> bool:
        if current_user.id != user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card_id} owned by another user.")
            abort(403)
        exists = self.user_card_repository.check_if_user_card_exists(card_id, user_id)
        logger.info(f"Checked if user card exists: card_id={card_id}, user_id={user_id}, exists={exists}")
        return exists

    def remove_user_card_from_album(self, card_id: int, album_id: int) -> None:
        logger.info(f"Attempting to remove user_card with ID {card_id} from album with ID {album_id}.")
        card: UserCard = self.user_card_repository.get_card(card_id)
        album: Album = self.album_reposiotry.get_album(album_id)
        if card is None or album is None:
            logger.error(f"User_card with ID {card_id} or ablum with ID {album_id} not found.")
            abort(404)
        elif current_user.id != card.user_id or current_user.id != album.user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card_id} owned by another user.")
            abort(403)
        else:
            self.user_card_repository.remove_user_card_from_album(card_id, album_id)
            logger.info(f"Removed user_card {card_id} from album {album_id} for user {current_user.id}")

    def add_user_card_to_album(self, card_id: int, album_id: int) -> None:
        card: UserCard = self.user_card_repository.get_card(card_id)
        album: Album = self.album_reposiotry.get_album(album_id)
        if card is None or album is None:
            logger.error(f"User_card with ID {card_id} or ablum with ID {album_id} not found.")
            abort(404)
        elif current_user.id != card.user_id or current_user.id != album.user_id:
            logger.warning(f"User {current_user.id} tried to access user_card {card_id} owned by another user.")
            abort(403)
        else:
            self.user_card_repository.add_user_card_to_album(card_id, album_id)
            logger.info(f"Added user_card {card_id} to album {album_id} for user {current_user.id}")

    def increase_user_card_availability(self, card_id: int) -> int:
        user_card = self.user_card_repository.get_card(card_id)
        if current_user.id != user_card.user_id:
            abort(403)
        else:
            new_availability = self.user_card_repository.increase_user_card_availability(card_id)
            return new_availability

    def decrease_user_card_availability(self, card_id: int) -> int:
        user_card = self.user_card_repository.get_card(card_id)
        if current_user.id != user_card.user_id:
            abort(403)
        elif user_card.availability == 0:
            return user_card.availability
        else:
            new_availability = self.user_card_repository.decrease_user_card_availability(card_id)
            return new_availability
