from flask import Blueprint

from src.basket.basket_controller import BasketController

bp = Blueprint('basket', __name__)

basket_controller = BasketController()
bp.add_url_rule('/', view_func=basket_controller.get_basket, methods=['GET', 'POST'])
bp.add_url_rule('/<int:basket_id>/add/<int:user_card_id>', view_func=basket_controller.add_user_card_to_basket,
                methods=['POST'])
bp.add_url_rule('/clear_basket', view_func=basket_controller.clear_basket, methods=['POST'])
bp.add_url_rule('/<int:basket_id>/delete_basket_item/<int:basket_item_id>',
                view_func=basket_controller.delete_basket_item, methods=['POST'])
bp.add_url_rule('/<int:basket_id>/item/<int:basket_item_id>/quantity/<int:quantity>',
                view_func=basket_controller.update_basket_item_quantity, methods=['POST'])
