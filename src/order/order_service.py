from flask import abort
from flask_login import current_user
from loguru import logger

from src.models import Order, OrderStateSet
from src.order.order_repository import OrderRepository


class OrderService:

    def __init__(self) -> None:
        self.order_repository: OrderService = OrderRepository()

    def get_orders(self, page: int, ROWS_PER_PAGE: int):
        logger.info(f"Retrieving orders.")
        orders = self.order_repository.get_orders(page, ROWS_PER_PAGE)
        logger.info(f"Retrieved orders orders.")
        return orders

    def get_order(self, order_id: int) -> Order:
        logger.info(f"Attempting to retrieve order with ID {order_id}.")
        order: Order = self.order_repository.get_order(order_id)
        if not order:
            logger.error(f"Order with ID {order_id} not found.")
            abort(404)
        elif current_user.id != order.user_id and current_user.id != order.customer_id:
            logger.warning(f"User {current_user.id} does not have permission to view order {order_id}.")
            abort(403)
        else:
            logger.info(f"Successfully retrieved order with ID {order_id}.")
            return order

    def get_order_items(self, order_id: int, page: int, ROWS_PER_PAGE: int):
        logger.info(f"Attempting to retrieve order items for order with ID {order_id}.")
        order: Order = self.order_repository.get_order(order_id)
        if current_user.id != order.user_id and current_user.id != order.customer_id:
            logger.warning(f"User {current_user.id} does not have permission to view order {order_id}.")
            abort(403)
        else:
            order_items = self.order_repository.get_order_items(order_id, page, ROWS_PER_PAGE)
            logger.info(f"Successfully retrieved order items for order with ID {order_id}.")
            return order_items

    def create_order(self, user_id, customer_id) -> None:
        logger.info(f"Attempting to create order by user {user_id} for customer {customer_id}.")
        if current_user.id != user_id and current_user.id != customer_id:
            logger.warning(
                f"Current user does not have permission to create order for user {user_id} and customer {customer_id}.")
            abort(403)
        else:
            logger.info(f"Creating new order for user {user_id} and customer {customer_id}.")
            self.order_repository.create_order(user_id, customer_id)

    def next_order_state(self, order_id) -> None:
        logger.info(f"Changing order state for order ID: {order_id}")
        self.order_repository.next_order_state(order_id)
        logger.info(f"Order state changed for order ID: {order_id}")

    def can_user_change_state(self, order: Order, user_id: int) -> bool:
        logger.info(f"Checking if user can change order state for order ID: {order.id}, user ID: {user_id}")

        states_to_change_by_user = {
            OrderStateSet.STATUS_1: "CUSTOMER",
            OrderStateSet.STATUS_2: "SELLER",
            OrderStateSet.STATUS_3: "CUSTOMER",
            OrderStateSet.STATUS_4: "SELLER",
        }

        user_type_with_permission = states_to_change_by_user.get(order.order_state)
        if user_type_with_permission == "CUSTOMER":
            logger.debug(f"Customer check for order state change for user ID: {user_id}")
            return self.is_current_user_customer_in_order(order, user_id)
        elif user_type_with_permission == "SELLER":
            logger.debug(f"Seller check for order state change for user ID: {user_id}")
            return self.is_current_user_seller_in_order(order, user_id)
        else:
            logger.warning(f"No permission defined for order state change for user ID: {user_id}")
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

    def get_orders_details_by_user_by_date(self, use_id: int) -> any:
        orders_details = self.order_repository.get_orders_details_by_user_by_date(use_id)
        return orders_details

    def get_orders_details_by_customer_by_date(self, use_id: int) -> any:
        orders_details = self.order_repository.get_orders_details_by_customer_by_date(use_id)
        return orders_details

