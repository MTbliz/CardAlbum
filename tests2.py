import requests
import json
from src.models import Card, CardColorEnum, CardMana, CardRarity, CardSet, CardDetails
from src.extensions import db
from run import app

BASE = "http://127.0.0.1:5000/"

# Create a new Card object
example_card = Card()

# Set the properties
example_card.title = "Example Card"
example_card.price = 10.0
example_card.availability = 100
example_card.type = "Creature"
example_card.image = b"example_image_binary_data" # Replace with actual binary data

# Create a new CardDetails object
example_card_details = CardDetails()

# Set the properties
example_card_details.color = CardColorEnum.BLUE
example_card_details.mana = CardMana.ONE
example_card_details.rarity = CardRarity.COMMON
example_card_details.set = CardSet.SET1
example_card_details.type = "Creature"
example_card_details.card_id = example_card.id

# Add the CardDetails object to the Card object
example_card.card_details = example_card_details

with app.app_context():
    # Add the objects to the session
    db.session.add(example_card)
    # Commit the changes
    db.session.commit()


#response = requests.post(BASE + "cards/card", json=card_json)
#print(response.json())
