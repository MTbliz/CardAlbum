from src.basket.basket_repository import BasketRepository
from src.models import Basket
from src.models import OrderItem


class BasketService:

    def __init__(self):
        self.basket_repository: BasketRepository = BasketRepository()

    def get_basket(self, basket_id: int) -> Basket:
        return self.basket_repository.get_basket(basket_id)

    def get_basket_by_user(self, user_id: int) -> Basket:
        return self.basket_repository.get_basket_by_user(user_id)

    def add_user_card_to_basket(self, basket_id: int, user_card_id: int) -> None:
        self.basket_repository.add_user_card_to_basket(basket_id, user_card_id)

    def get_basket_items_by_user(self, user_id: int, page: int, ROWS_PER_PAGE: int):
        return self.basket_repository.get_basket_items_by_user(user_id, page, ROWS_PER_PAGE)

    def clear_basket(self, user_id: int) -> None:
        self.basket_repository.clear_basket(user_id)

    def update_basket_item_quantity(self, user_id: int, basket_id: int, basket_item_id: int, quantity: int):
        self.basket_repository.update_basket_item_quantity(user_id, basket_id, basket_item_id, quantity)

    def get_basket_items_count(self, user_id: int) -> int:
        return self.basket_repository.get_basket_items_count(user_id)

    def delete_basket_item(self, basket_id: int, basket_item_id: int) -> None:
        self.basket_repository.delete_basket_item(basket_id, basket_item_id)

