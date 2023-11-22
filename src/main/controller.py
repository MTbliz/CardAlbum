from flask import render_template, jsonify, request
from src.models import Card

from src.main.service import CardService, AlbumService


class CardsController:

    def __init__(self):
        self.card_service = CardService()

    def cards(self):
        cards = self.card_service.get_cards()
        return str(cards)

    def create_card(self):
        data = request.get_json()
        card = Card(**data)
        self.card_service.add_card(card)
        return str(card), 201




