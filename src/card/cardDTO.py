from src.models import Card, UserCard, CardDetails, CardColor, CardSet, CardMana, CardQuality, CardRarity, CardColorEnum


class CardDTO:

    def __init__(self, title, colors, mana, rarity, card_set, card_type):
        self.title = title
        self.colors = colors
        self.mana = mana
        self.rarity = rarity
        self.card_set = card_set
        self.card_type = card_type

    def to_card(self):
        colors = [CardColorEnum(color).name for color in self.colors]
        mana = CardMana(str(self.mana)).name
        rarity = CardRarity(self.rarity).name
        card_set = CardSet(self.card_set).name

        card = Card()
        card.title = self.title
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


class UserCardDTO:

    def __init__(self, card, price, availability, quality, user_id):
        self.card = card
        self.price = price
        self.availability = availability
        self.quality = quality
        self.user_id = user_id

    def to_user_card(self):
        quality = self.quality
        user_card = UserCard()
        user_card.price = self.price
        user_card.availability = self.availability
        user_card.quality = quality
        user_card.card = self.card
        user_card.user_id = self.user_id
        return user_card
