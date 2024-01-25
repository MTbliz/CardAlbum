from src.card.user_card_repository import UserCardRepository
from src.models import UserCard


class UserCardService:

    def __init__(self) -> None:
        self.user_card_repository: UserCardRepository = UserCardRepository()

    def get_cards(self, user_id: int, field_sort: str, order: str, filters: dict[str, str], page: int,
                  ROWS_PER_PAGE: int):
        return self.user_card_repository.get_cards(user_id, field_sort, order, filters, page, ROWS_PER_PAGE)

    def get_card(self, card_id: int) -> UserCard:
        return self.user_card_repository.get_card(card_id)

    def add_card(self, card: UserCard) -> None:
        self.user_card_repository.add_card(card)

    def delete_card(self, card_id: int) -> None:
        self.user_card_repository.delete_card(card_id)

    def check_if_user_card_exists(self, card_id: int, user_id: int) -> bool:
        return self.user_card_repository.check_if_user_card_exists(card_id, user_id)

    def remove_user_card_from_album(self, card_id: int, album_id: int) -> None:
        return self.user_card_repository.remove_user_card_from_album(card_id, album_id)

    def add_user_card_to_album(self, card_id: int, album_id: int) -> None:
        return self.user_card_repository.add_user_card_to_album(card_id, album_id)
