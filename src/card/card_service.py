from src.card.card_repository import CardRepository


class CardService:

    def __init__(self):
        self.card_repository = CardRepository()

    def get_cards(self):
        return self.card_repository.get_cards()

    def get_card(self, card_id):
        return self.card_repository.get_card(card_id)

    def add_card(self, card):
        return self.card_repository.add_card(card)

    def delete_card(self, card_id):
        return self.card_repository.delete_card(card_id)
