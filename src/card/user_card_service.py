from flask import abort
from flask_login import current_user

from src.album.album_repository import AlbumRepository
from src.card.user_card_repository import UserCardRepository
from src.models import UserCard, Album


class UserCardService:

    def __init__(self) -> None:
        self.user_card_repository: UserCardRepository = UserCardRepository()
        self.album_reposiotry: AlbumRepository = AlbumRepository()

    def get_cards(self, user_id: int, field_sort: str, order: str, filters: dict[str, str], page: int,
                  ROWS_PER_PAGE: int):
        return self.user_card_repository.get_cards(user_id, field_sort, order, filters, page, ROWS_PER_PAGE)

    def get_card(self, card_id: int) -> UserCard:
        user_card = self.user_card_repository.get_card(card_id)
        if not user_card:
            abort(404)
        elif current_user.id != user_card.user_id:
            abort(403)
        else:
            user_card

    def add_card(self, card: UserCard) -> None:
        if current_user.id != card.user_id:
            abort(403)
        else:
            self.user_card_repository.add_card(card)

    def delete_card(self, card_id: int) -> None:
        card: UserCard = self.user_card_repository.get_card(card_id)
        if card is None:
            abort(404)
        elif current_user.id != card.user_id:
            abort(403)
        else:
            self.user_card_repository.delete_card(card_id)

    def check_if_user_card_exists(self, card_id: int, user_id: int) -> bool:
        if current_user.id != user_id:
            abort(403)
        return self.user_card_repository.check_if_user_card_exists(card_id, user_id)

    def remove_user_card_from_album(self, card_id: int, album_id: int) -> None:
        card: UserCard = self.user_card_repository.get_card(card_id)
        album: Album = self.album_reposiotry.get_album(album_id)
        if card is None or album is None:
            abort(404)
        elif current_user.id != card.user_id or current_user.id != album.user_id:
            abort(403)
        else:
            return self.user_card_repository.remove_user_card_from_album(card_id, album_id)

    def add_user_card_to_album(self, card_id: int, album_id: int) -> None:
        card: UserCard = self.user_card_repository.get_card(card_id)
        album: Album = self.album_reposiotry.get_album(album_id)
        if card is None or album is None:
            abort(404)
        elif current_user.id != card.user_id or current_user.id != album.user_id:
            abort(403)
        else:
            return self.user_card_repository.add_user_card_to_album(card_id, album_id)
