from sqlalchemy import func

from src import db
from src.models import Basket, BasketItem


class BasketRepository:

    def get_basket(self, basket_id: int) -> Basket:
        basket: Basket = Basket.query.get(basket_id)
        return basket

    def get_basket_by_user(self, user_id: int) -> Basket:
        basket: Basket = Basket.query.filter_by(user_id=user_id).first()
        return basket

    def add_user_card_to_basket(self, basket_id: int, user_card_id: int) -> None:
        basket: Basket = Basket.query.get(basket_id)
        basket_item: BasketItem = BasketItem.query.filter_by(user_card_id=user_card_id).first()
        if basket_item:
            basket_item.quantity = basket_item.quantity + 1
        else:
            basket_item = BasketItem(basket_id=basket.id, user_card_id=user_card_id, quantity=1)
            db.session.add(basket_item)
        db.session.commit()

    def get_basket_items_by_user(self, user_id: int, page: int, ROWS_PER_PAGE: int):
        basket_items = BasketItem.query.join(Basket).filter(Basket.user_id == user_id) \
            .paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
        return basket_items

    def clear_basket(self, user_id: int) -> None:
        # Get the IDs of the rows to delete
        ids_to_delete = db.session.query(BasketItem.id).join(Basket).filter(Basket.user_id == user_id).subquery()
        # Delete the rows based on the IDs
        BasketItem.query.filter(BasketItem.id.in_(ids_to_delete)).delete()
        # Commit the changes
        db.session.commit()

    def update_basket_item_quantity(self, user_id: int, basket_id: int, basket_item_id: int, quantity: int) -> None:
        basket_item: BasketItem = BasketItem.query \
            .join(Basket) \
            .filter(Basket.id == basket_id, Basket.user_id == user_id, BasketItem.id == basket_item_id).first()
        if basket_item:
            basket_item.quantity = quantity
            db.session.commit()

    def get_basket_items_count(self, user_id: int) -> int:
        basket_count: int = BasketItem.query.join(Basket).filter(Basket.user_id == user_id).with_entities(
            func.sum(BasketItem.quantity)).scalar()
        if basket_count is None:
            basket_count = 0
        return basket_count

    def delete_basket_item(self, basket_id: int, basket_item_id: int) -> bool:
        basket_item: BasketItem = BasketItem.query \
            .filter(BasketItem.basket_id == basket_id, BasketItem.id == basket_item_id).first()
        if not basket_item:
            return False
        else:
            db.session.delete(basket_item)
            db.session.commit()
            return True
