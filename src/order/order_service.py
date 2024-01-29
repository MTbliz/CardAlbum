from flask import abort
from flask_login import current_user

from src.models import Order, OrderStateSet
from src.order.order_repository import OrderRepository


class OrderService:

    def __init__(self) -> None:
        self.order_repository: OrderService = OrderRepository()

    def get_orders(self, page: int, ROWS_PER_PAGE: int):
        return self.order_repository.get_orders(page, ROWS_PER_PAGE)

    def get_order(self, order_id: int) -> Order:
        order: Order = self.order_repository.get_order(order_id)
        if not order:
            abort(404)
        elif current_user.id != order.user_id and current_user.id != order.customer_id:
            abort(403)
        else:
            return order

    def get_order_items(self, order_id: int, page: int, ROWS_PER_PAGE: int):
        order: Order = self.order_repository.get_order(order_id)
        if current_user.id != order.user_id and order.customer_id:
            abort(403)
        else:
            return self.order_repository.get_order_items(order_id, page, ROWS_PER_PAGE)

    def create_order(self, user_id, customer_id) -> None:
        if current_user.id != user_id and current_user.id != customer_id:
            abort(403)
        else:
            self.order_repository.create_order(user_id, customer_id)

    def next_order_state(self, order_id) -> None:
        self.order_repository.next_order_state(order_id)

    def can_user_change_state(self, order: Order, user_id: int) -> bool:

        states_to_change_by_user = {
            OrderStateSet.STATUS_1: "CUSTOMER",
            OrderStateSet.STATUS_2: "SELLER",
            OrderStateSet.STATUS_3: "CUSTOMER",
            OrderStateSet.STATUS_4: "SELLER",
        }

        user_type_with_permission = states_to_change_by_user.get(order.order_state)
        if user_type_with_permission == "CUSTOMER":
            return self.is_current_user_customer_in_order(order, user_id)
        elif user_type_with_permission == "SELLER":
            return self.is_current_user_seller_in_order(order, user_id)
        else:
            return False

    def is_current_user_customer_in_order(self, order: Order, user_id: int) -> bool:
        if order.customer_id == user_id:
            return True
        else:
            return False

    def is_current_user_seller_in_order(self, order: Order, user_id: int) -> bool:
        if order.user_id == user_id:
            return True
        else:
            return False

