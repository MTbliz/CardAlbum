from flask import abort
from flask_login import current_user

from src.basket.basket_repository import BasketRepository
from src.models import Basket, BasketItem
from src.card.user_card_repository import UserCardRepository


class BasketService:

    def __init__(self):
        self.basket_repository: BasketRepository = BasketRepository()
        self.user_card_repository: UserCardRepository = UserCardRepository()

    def get_basket(self, basket_id: int) -> Basket:
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if not basket:
            abort(404)
        elif current_user.id != basket.user_id:
            abort(403)
        else:
            return basket

    def get_basket_by_user(self, user_id: int) -> Basket:
        basket: Basket = self.basket_repository.get_basket_by_user(user_id)
        if not basket:
            abort(404)
        elif current_user.id != basket.user_id:
            abort(403)
        else:
            return basket

    def add_user_card_to_basket(self, basket_id: int, user_card_id: int) -> None:
        basket: Basket = self.basket_repository.get_basket(basket_id)
        user_card = self.user_card_repository.get_card(user_card_id)
        if basket is None or user_card is None:
            abort(404)
        elif current_user.id != user_card.user_id or current_user.id != basket.user_id:
            abort(403)
        else:
            self.basket_repository.add_user_card_to_basket(basket_id, user_card_id)

    def get_basket_items_by_user(self, user_id: int, page: int, ROWS_PER_PAGE: int):
        return self.basket_repository.get_basket_items_by_user(user_id, page, ROWS_PER_PAGE)

    def clear_basket(self, user_id: int) -> None:
        if current_user.id != user_id:
            abort(403)
        else:
            self.basket_repository.clear_basket(user_id)

    def update_basket_item_quantity(self, user_id: int, basket_id: int, basket_item_id: int, quantity: int):
        basket_item: BasketItem = self.basket_repository.get_basket_item(basket_item_id)
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if basket_item is None or basket:
            abort(404)
        elif any(current_user.id != user_id for user_id in [user_id, basket_item.basket.user_id, basket.user_id]):
            abort(403)
        else:
            self.basket_repository.update_basket_item_quantity(user_id, basket_id, basket_item_id, quantity)

    def get_basket_items_count(self, user_id: int) -> int:
        if current_user.id != user_id:
            abort(403)
        else:
            return self.basket_repository.get_basket_items_count(user_id)

    def delete_basket_item(self, basket_id: int, basket_item_id: int) -> None:
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if basket is None:
            abort(404)
        elif current_user.id != basket.user_id:
            abort(403)
        else:
            self.basket_repository.delete_basket_item(basket_id, basket_item_id)
