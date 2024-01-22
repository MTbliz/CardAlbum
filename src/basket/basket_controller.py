from flask import request, session, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user
from src import db
from src.models import User, UserCard, Basket, BasketItem
from src.basket.basket_forms import BasketSellForm
from src.basket.basket_service import BasketService


class BasketController:

    def __init__(self):
        self.basket_service = BasketService()

    def get_basket(self):
        page = request.args.get('page', 1, type=int)
        ROWS_PER_PAGE = 5

        form = BasketSellForm()

        basket_items = self.basket_service.get_basket_items_by_user(current_user.id, page, ROWS_PER_PAGE)
        customers = User.query.filter(User.id != current_user.id).all()
        customer_choices = [(customer.id, customer.email) for customer in customers]
        total_price = sum(item.quantity * item.user_card.price for item in basket_items.items)
        form.customer.choices = customer_choices
        form.total_price.data = total_price

        if form.validate_on_submit():
            user_id = current_user.id
            self.basket_service.clear_basket(user_id)
            session['basket_count'] = 0
            flash("Order created successfully", "success")
            return redirect(url_for('main.root'))

        return render_template('basket/basket_page.html',
                               basket_items=basket_items,
                               url_view="basket.get_basket",
                               form=form,
                               customers=customers, params={})

    def add_user_card_to_basket(self, basket_id, user_card_id):
        self.basket_service.add_user_card_to_basket(basket_id, user_card_id)
        basket_count = int(session['basket_count'])
        session['basket_count'] = basket_count + 1
        return "Item added to basket", 200

    def delete_basket_item(self, basket_id, basket_item_id):
        self.basket_service.delete_basket_item(basket_id, basket_item_id)
        user_id = current_user.id
        basket_count = self.basket_service.get_basket_items_count(user_id)
        session['basket_count'] = basket_count
        return redirect(url_for('basket.get_basket'))

    def clear_basket(self):
        user_id = current_user.id
        self.basket_service.clear_basket(user_id)
        session['basket_count'] = 0
        flash("All products removed successfully", "success")
        return redirect(url_for('basket.get_basket'))

    def update_basket_item_quantity(self, basket_id, basket_item_id, quantity):
        user_id = current_user.id
        self.basket_service.update_basket_item_quantity(user_id, basket_id, basket_item_id, quantity)
        basket_count = self.basket_service.get_basket_items_count(user_id)
        session['basket_count'] = basket_count
        return jsonify({"basket_count": session['basket_count']}), 200




