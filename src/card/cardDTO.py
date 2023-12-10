from src.models import Card, CardDetails, CardColor, CardSet, CardMana, CardQuality, CardRarity, CardColorEnum

class CardDTO:

    def __init__(self, title, colors, mana, rarity, card_set, card_type, quality, price, availability):
        self.title = title
        self.colors = colors
        self.mana = mana
        self.rarity = rarity
        self.card_set = card_set
        self.card_type = card_type
        self.quality = quality
        self.price = price
        self.availability = availability

    def to_card(self):
        colors = [CardColorEnum(color).name for color in self.colors]
        mana = CardMana(str(self.mana)).name
        rarity = CardRarity(self.rarity).name
        card_set = CardSet(self.card_set).name

        card = Card()
        card.title = self.title
        card.price = self.price
        card.availability = self.availability
        card.type = self.card_type

        card_details = CardDetails()
        new_colors = [CardColor(color=color) for color in colors]
        card_details.colors = new_colors
        card_details.mana = mana
        card_details.rarity = rarity
        card_details.set = card_set
        card_details.type = self.card_type
        card_details.card_id = card.id

        card.card_details = card_details
        return card
