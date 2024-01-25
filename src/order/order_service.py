from src.models import Order
from src.order.order_repository import OrderRepository


class OrderService:

    def __init__(self) -> None:
        self.order_repository: OrderService = OrderRepository()

    def get_orders(self, page: int, ROWS_PER_PAGE: int):
        return self.order_repository.get_orders(page, ROWS_PER_PAGE)

    def get_order(self, order_id: int) -> Order:
        return self.order_repository.get_order(order_id)

    def get_order_items(self, order_id: int, page: int, ROWS_PER_PAGE: int):
        return self.order_repository.get_order_items(order_id, page, ROWS_PER_PAGE)

    def create_order(self, user_id, customer_id) -> None:
        self.order_repository.create_order(user_id, customer_id)

    def next_order_state(self, order_id) -> None:
        self.order_repository.next_order_state(order_id)
