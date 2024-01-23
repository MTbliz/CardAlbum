from datetime import datetime

from src import db
from src.models import Order, OrderItem, Basket, BasketItem, OrderStateSet


class OrderRepository:

    def get_order(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        return order

    def get_orders(self, page, ROWS_PER_PAGE):
        orders = Order.query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
        return orders

    def get_order_items(self, order_id, page, ROWS_PER_PAGE):
        order_items = OrderItem.query.filter_by(order_id=order_id).paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)
        return order_items

    def create_order(self, user_id, customer_id):
        # Assume you have a list of basket items
        basket_items = BasketItem.query.join(Basket).filter(Basket.user_id == user_id) \
            .all()

        total_price = 0
        for basket_item in basket_items:
            total_price += basket_item.total_price
        # Create a new order
        order = Order(
            total_price=total_price,  # Replace with actual total price
            order_state=OrderStateSet.STATUS_1,  # Replace with actual order state
            user_id=user_id,  # Replace with actual user id
            customer_id=customer_id,  # Replace with actual customer id
            order_date=datetime.utcnow()  # Current date and time
        )

        # Create order items and append them to the order
        for basket_item in basket_items:
            order_item = OrderItem(
                order=order,  # Pass the order instance here
                user_card_id=basket_item.user_card_id,
                quantity=basket_item.quantity
            )
            order.order_items.append(order_item)
        # Add the order to the session
        db.session.add(order)

        # Commit the transaction
        db.session.commit()

    def next_order_state(self, order_id):
        order: Order = Order.query.filter_by(id=order_id).first()
        order_state_name: str = order.order_state.name
        order_state_prefix: str = order_state_name.split("_")[0]

        order_state_number = int(order_state_name.split("_")[1])
        if order_state_number != len(OrderStateSet):
            new_order_state_number = order_state_number + 1
            new_order_state = f"{order_state_prefix}_{new_order_state_number}"
            order.order_state = getattr(OrderStateSet, new_order_state.upper())
            db.session.commit()