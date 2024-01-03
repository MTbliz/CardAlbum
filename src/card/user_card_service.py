from src.card.user_card_repository import UserCardRepository


class UserCardService:

    def __init__(self):
        self.user_card_repository = UserCardRepository()

    def get_cards(self, field_sort, order, filters, page, ROWS_PER_PAGE):
        return self.user_card_repository.get_cards(field_sort, order, filters, page, ROWS_PER_PAGE)

    def get_card(self, card_id):
        return self.user_card_repository.get_card(card_id)

    def add_card(self, card):
        return self.user_card_repository.add_card(card)

    def delete_card(self, card_id):
        return self.user_card_repository.delete_card(card_id)

    def check_if_user_card_exists(self, card_id, user):
        return self.user_card_repository.check_if_user_card_exists(card_id, user)

    def remove_user_card_from_album(self, card_id, album_id):
        return self.user_card_repository.remove_user_card_from_album(card_id, album_id)

    def add_user_card_to_album(self, card_id, album_id):
        return self.user_card_repository.add_user_card_to_album(card_id, album_id)

