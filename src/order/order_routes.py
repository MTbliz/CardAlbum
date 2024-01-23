from flask import Blueprint

from src.order.order_controller import OrderController

bp = Blueprint('order', __name__)

order_controller = OrderController()
bp.add_url_rule('/', view_func=order_controller.orders, methods=['GET'])
bp.add_url_rule('/order/<int:order_id>', view_func=order_controller.get_order, methods=['GET'])
bp.add_url_rule('/order/next/<int:order_id>', view_func=order_controller.next_order_state, methods=['POST'])
