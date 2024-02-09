from typing import Union

from flask import request, session, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from src.basket.basket_forms import BasketSellForm
from src.basket.basket_service import BasketService
from src.models import User
from src.order.order_service import OrderService
from src.user.user_service import UserService


class BasketController:

    def __init__(self):
        self.basket_service: BasketService = BasketService()
        self.order_service: OrderService = OrderService()
        self.user_service: UserService = UserService()

    @login_required
    def get_basket(self) -> Union[str, Response]:
        page: int = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE: int = 5

        form: BasketSellForm = BasketSellForm()

        basket_items = self.basket_service.get_basket_items_by_user(current_user.id, page, ROWS_PER_PAGE)
        customers: list[User] = self.user_service.get_possible_customers(current_user.id)
        customer_choices: list[tuple[int, str]] = [(customer.id, customer.email) for customer in customers]
        total_price: float = sum(item.quantity * item.user_card.price for item in basket_items.items)
        form.customer.choices = customer_choices
        form.total_price.data = total_price

        if form.validate_on_submit():
            user_id: int = current_user.id
            customer_id: int = request.form.get("customer", type=int)
            self.order_service.create_order(user_id, customer_id)
            self.basket_service.clear_basket(user_id)
            session['basket_count'] = 0
            flash("Order created successfully", "success")
            return redirect(url_for('main.root'))

        return render_template('basket/basket_page.html',
                               basket_items=basket_items,
                               url_view="basket.get_basket",
                               form=form,
                               customers=customers, params={})

    @login_required
    def add_user_card_to_basket(self, basket_id: int, user_card_id: int) -> str:
        self.basket_service.add_user_card_to_basket(basket_id, user_card_id)
        basket_count: int = int(session.get('basket_count', 0))
        session['basket_count'] = basket_count + 1
        return "Item added to basket", 200

    @login_required
    def delete_basket_item(self, basket_id: int, basket_item_id: int) -> Response:
        self.basket_service.delete_basket_item(basket_id, basket_item_id)
        user_id: int = current_user.id
        basket_count: int = self.basket_service.get_basket_items_count(user_id)
        session['basket_count'] = basket_count
        return redirect(url_for('basket.get_basket'))

    @login_required
    def clear_basket(self) -> Response:
        user_id: int = current_user.id
        self.basket_service.clear_basket(user_id)
        session['basket_count'] = 0
        flash("All products removed successfully", "success")
        return redirect(url_for('basket.get_basket'))

    @login_required
    def update_basket_item_quantity(self, basket_id: int, basket_item_id: int, quantity: int) -> str:
        user_id: int = current_user.id
        self.basket_service.update_basket_item_quantity(user_id, basket_id, basket_item_id, quantity)
        basket_count: int = self.basket_service.get_basket_items_count(user_id)
        session['basket_count'] = basket_count
        return jsonify({"basket_count": session['basket_count']}), 200
