from flask import abort
from flask_login import current_user
from loguru import logger

from src.basket.basket_repository import BasketRepository
from src.models import Basket, BasketItem
from src.card.user_card_repository import UserCardRepository


class BasketService:

    def __init__(self):
        self.basket_repository: BasketRepository = BasketRepository()
        self.user_card_repository: UserCardRepository = UserCardRepository()

    def get_basket(self, basket_id: int) -> Basket:
        logger.info(f"Retrieving basket with ID: {basket_id}")
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if not basket:
            logger.error(f"Basket with ID: {basket_id} not found.")
            abort(404)
        elif current_user.id != basket.user_id:
            logger.warning(f"User {current_user.id} attempted to access a basket not belonging to them.")
            abort(403)
        else:
            logger.info(f"Successfully retrieved basket with ID: {basket_id}")
            return basket

    def get_basket_by_user(self, user_id: int) -> Basket:
        logger.info(f"Retrieving basket for user: {user_id}")
        basket: Basket = self.basket_repository.get_basket_by_user(user_id)
        if not basket:
            logger.error(f"Basket fur user: {user_id} not found.")
            abort(404)
        elif current_user.id != basket.user_id:
            logger.warning(f"User {current_user.id} attempted to access a basket not belonging to them.")
            abort(403)
        else:
            logger.info(f"Successfully retrieved basket with ID: {basket.id}")
            return basket

    def add_user_card_to_basket(self, basket_id: int, user_card_id: int) -> None:
        logger.info(f"Adding user card with ID {user_card_id} to basket with ID {basket_id}")
        basket: Basket = self.basket_repository.get_basket(basket_id)
        user_card = self.user_card_repository.get_card(user_card_id)
        if basket is None or user_card is None:
            logger.error("Failed to add user card to basket due to missing basket or user card.")
            abort(404)
        elif current_user.id != user_card.user_id or current_user.id != basket.user_id:
            logger.warning("User attempted to add a card to a basket they do not own.")
            abort(403)
        else:
            self.basket_repository.add_user_card_to_basket(basket_id, user_card_id)
            logger.info(f"Successfully added user card to basket.")

    def get_basket_items_by_user(self, user_id: int, page: int, ROWS_PER_PAGE: int):
        logger.info(f"Retrieving basket items for user: {user_id}")
        basket_items = self.basket_repository.get_basket_items_by_user(user_id, page, ROWS_PER_PAGE)
        logger.info(f"Successfully retrieved basket items for user: {user_id}")
        return basket_items

    def clear_basket(self, user_id: int) -> None:
        logger.info(f"Clearing basket for user with ID: {user_id}")
        if current_user.id != user_id:
            logger.warning(f"User {current_user.id} attempted to clear a basket not belonging to them.")
            abort(403)
        else:
            self.basket_repository.clear_basket(user_id)
            logger.info(f"Successfully cleared basket for user with ID: {user_id}")

    def update_basket_item_quantity(self, user_id: int, basket_id: int, basket_item_id: int, quantity: int):
        logger.info("Updating quantity for basket item.")
        basket_item: BasketItem = self.basket_repository.get_basket_item(basket_item_id)
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if basket_item is None or basket:
            logger.error("Basket item or basket not found.")
            abort(404)
        elif any(current_user.id != user_id for user_id in [user_id, basket_item.basket.user_id, basket.user_id]):
            logger.warning("Unauthorized attempt to update basket item quantity.")
            abort(403)
        else:
            self.basket_repository.update_basket_item_quantity(user_id, basket_id, basket_item_id, quantity)
            logger.info("Quantity updated successfully for basket item.")

    def get_basket_items_count(self, user_id: int) -> int:
        if current_user.id != user_id:
            logger.warning("Unauthorized attempt to retrieve basket items count.")
            abort(403)
        else:
            count = self.basket_repository.get_basket_items_count(user_id)
            logger.info(f"Retrieved basket items count: {count} for user.")
            return count

    def delete_basket_item(self, basket_id: int, basket_item_id: int) -> None:
        logger.info("Deleting basket item.")
        basket: Basket = self.basket_repository.get_basket(basket_id)
        if basket is None:
            logger.error("Basket not found.")
            abort(404)
        elif current_user.id != basket.user_id:
            logger.warning("Unauthorized attempt to delete basket item.")
            abort(403)
        else:
            self.basket_repository.delete_basket_item(basket_id, basket_item_id)
            logger.info("Basket item deleted successfully.")
