from datetime import datetime

from src import db
from src.models import Order, OrderItem, Basket, BasketItem, OrderStateSet


class OrderRepository:

    def get_order(self, order_id: int) -> Order:
        order: Order = Order.query.filter_by(id=order_id).first()
        return order

    def get_orders(self, page: int, ROWS_PER_PAGE: int):
        orders = Order.query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
        return orders

    def get_order_items(self, order_id: int, page: int, ROWS_PER_PAGE: int):
        order_items = OrderItem.query.filter_by(order_id=order_id).paginate(page=page, per_page=ROWS_PER_PAGE,
                                                                            error_out=False)
        return order_items

    def create_order(self, user_id: int, customer_id: int) -> None:
        # Assume you have a list of basket items
        basket_items: list[BasketItem] = BasketItem.query.join(Basket).filter(Basket.user_id == user_id) \
            .all()

        total_price: int = 0
        for basket_item in basket_items:
            total_price += basket_item.total_price
        # Create a new order
        order: Order = Order(
            total_price=total_price,
            order_state=OrderStateSet.STATUS_1,
            user_id=user_id,
            customer_id=customer_id,
            order_date=datetime.utcnow()
        )

        # Create order items and append them to the order
        for basket_item in basket_items:
            order_item: OrderItem = OrderItem(
                order=order,
                card_id=basket_item.user_card.card_id,
                quantity=basket_item.quantity,
                quality=basket_item.user_card.quality,
                total_price=basket_item.total_price
            )
            order.order_items.append(order_item)
        db.session.add(order)
        db.session.commit()

    def next_order_state(self, order_id: int) -> None:
        order: Order = Order.query.filter_by(id=order_id).first()
        order_state_name: str = order.order_state.name
        order_state_prefix: str = order_state_name.split("_")[0]

        order_state_number = int(order_state_name.split("_")[1])
        if order_state_number != len(OrderStateSet):
            new_order_state_number = order_state_number + 1
            new_order_state = f"{order_state_prefix}_{new_order_state_number}"
            order.order_state = getattr(OrderStateSet, new_order_state.upper())
            db.session.commit()
