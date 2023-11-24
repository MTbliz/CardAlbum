from flask import Blueprint
from src.card.card_controller import CardsController

bp = Blueprint('card', __name__)

cards_controller = CardsController()
bp.add_url_rule('/', view_func=cards_controller.cards)
bp.add_url_rule('/card', view_func=cards_controller.create_card, methods=['POST'])