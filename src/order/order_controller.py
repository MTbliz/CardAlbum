from flask import render_template, url_for, request, redirect, flash
from flask_login import current_user
from werkzeug.wrappers import Response

from src.basket.basket_service import BasketService
from src.models import OrderStateSet, Order
from src.order.order_service import OrderService


class OrderController:

    def __init__(self) -> None:
        self.basket_service: BasketService = BasketService()
        self.order_service: OrderService = OrderService()

    def orders(self) -> str:
        page: int = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE: int = 5
        orders = self.order_service.get_orders(page, ROWS_PER_PAGE)
        return render_template("orders/orders.html",
                               orders=orders,
                               url_view="order.orders",
                               params={})

    def get_order(self, order_id: int) -> str:
        page: int = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE: int = 5
        order_items = self.order_service.get_order_items(order_id, page, ROWS_PER_PAGE)
        order: Order = self.order_service.get_order(order_id)
        total_price: float = order.total_price
        order_state_name: str = order.order_state.name
        order_state_number = int(order_state_name.split("_")[1])
        all_states: int = len(OrderStateSet)
        progress_percent: float = order_state_number / all_states * 100
        change_state_possible = self.order_service.can_user_change_state(order, current_user.id)
        return render_template("order.html",
                               order=order,
                               order_items=order_items,
                               progress_percent=progress_percent,
                               total_price=total_price,
                               change_state_possible=change_state_possible,
                               url_view="order.get_order",
                               params={"order_id": order_id})

    def next_order_state(self, order_id: int) -> Response:
        order: Order = self.order_service.get_order(order_id)
        change_possible = self.order_service.can_user_change_state(order, current_user.id)
        if change_possible:
            self.order_service.next_order_state(order_id)
            flash("State changed successfully", "success")
        else:
            flash("Not enough permission to change state", "danger")
        return redirect(url_for("order.get_order", order_id=order_id))
