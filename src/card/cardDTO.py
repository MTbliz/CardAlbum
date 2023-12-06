from src.models import Card, CardDetails, CardSet, CardMana, CardQuality, CardRarity, CardColor

class CardDTO:

    def __init__(self, title, color, mana, rarity, card_set, card_type, quality, price, availability):
        self.title = title
        self.color = color
        self.mana = mana
        self.rarity = rarity
        self.card_set = card_set
        self.card_type = card_type
        self.quality = quality
        self.price = price
        self.availability = availability

    def to_card(self):
        color = CardColor(self.color).name
        mana = CardMana(str(self.mana)).name
        rarity = CardRarity(self.rarity).name
        card_set = CardSet(self.card_set).name

        card = Card()
        card.title = self.title
        card.price = self.price
        card.availability = self.availability
        card.type = self.card_type

        card_details = CardDetails()
        card_details.color = color
        card_details.mana = mana
        card_details.rarity = rarity
        card_details.set = card_set
        card_details.type = self.card_type
        card_details.card_id = card.id

        card.card_details = card_details
        return card
