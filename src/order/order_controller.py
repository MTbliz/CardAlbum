from flask import render_template, url_for, request, redirect
from flask_login import current_user

from src.basket.basket_service import BasketService
from src.order.order_service import OrderService
from src.models import OrderStateSet


class OrderController:

    def __init__(self):
        self.basket_service = BasketService()
        self.order_service = OrderService()

    def orders(self):
        page = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE = 5
        orders = self.order_service.get_orders(page, ROWS_PER_PAGE)
        return render_template("orders/orders.html",
                               orders=orders,
                               url_view="order.orders",
                               params={})

    def get_order(self, order_id):

        page = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE = 5
        order_items = self.order_service.get_order_items(order_id, page, ROWS_PER_PAGE)
        order = self.order_service.get_order(order_id)
        total_price = order.total_price
        order_state_name: str = order.order_state.name
        order_state_number = int(order_state_name.split("_")[1])
        all_states = len(OrderStateSet)
        progress_percent = order_state_number / all_states * 100
        return render_template("order.html",
                               order=order,
                               order_items=order_items,
                               progress_percent=progress_percent,
                               total_price=total_price,
                               url_view="order.get_order",
                               params={"order_id": order_id})

    def next_order_state(self, order_id):
        self.order_service.next_order_state(order_id)
        return redirect(url_for("order.get_order", order_id=order_id))