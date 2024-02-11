from flask import Blueprint

from src.card.card_controller import CardsController

bp = Blueprint('card', __name__)

cards_controller = CardsController()
bp.add_url_rule('/', view_func=cards_controller.cards, methods=['GET', 'POST'])
bp.add_url_rule('/card', view_func=cards_controller.create_card, methods=['GET', 'POST'])
bp.add_url_rule('/card/<id>', view_func=cards_controller.delete_user_card, methods=['GET'])
bp.add_url_rule('/card/<card_id>/<album_id>', view_func=cards_controller.remove_user_card_from_album, methods=['GET'])
bp.add_url_rule('/card/add/<card_id>/<album_id>', view_func=cards_controller.add_user_card_to_album,
                methods=['GET', 'POST'])
bp.add_url_rule('/card/<card_id>/increase', view_func=cards_controller.increase_user_card_availability, methods=['POST'])
bp.add_url_rule('/card/<card_id>/decrease', view_func=cards_controller.decrease_user_card_availability, methods=['POST'])
bp.before_request(cards_controller.store_or_clear_endpoint)
