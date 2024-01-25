from src.models import Card, UserCard, CardDetails, CardColor, CardSet, CardMana, CardRarity, CardColorEnum


class CardDTO:

    def __init__(self, title: str, colors: list[str], mana: str, rarity: str, card_set: str, card_type: str) -> None:
        self.title: str = title
        self.colors: list[str] = colors
        self.mana: str = mana
        self.rarity: str = rarity
        self.card_set: str = card_set
        self.card_type: str = card_type

    def to_card(self) -> Card:
        colors: list[str] = [CardColorEnum(color).name for color in self.colors]
        mana: str = CardMana(str(self.mana)).name
        rarity: str = CardRarity(self.rarity).name
        card_set: str = CardSet(self.card_set).name

        card: Card = Card()
        card.title = self.title
        card.type = self.card_type

        card_details: CardDetails = CardDetails()
        new_colors: list[CardColor] = [CardColor(color=color) for color in colors]
        card_details.colors = new_colors
        card_details.mana = mana
        card_details.rarity = rarity
        card_details.set = card_set
        card_details.type = self.card_type
        card_details.card_id = card.id

        card.card_details = card_details
        return card


class UserCardDTO:

    def __init__(self, card: Card, price: float, availability: int, quality: str, user_id: int) -> None:
        self.card = card
        self.price = price
        self.availability = availability
        self.quality = quality
        self.user_id = user_id

    def to_user_card(self) -> UserCard:
        quality: str = self.quality
        user_card: UserCard = UserCard()
        user_card.price = self.price
        user_card.availability = self.availability
        user_card.quality = quality
        user_card.card = self.card
        user_card.user_id = self.user_id
        return user_card
