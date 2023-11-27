from flask import request, render_template
from src.models import Card

from src.card.card_service import CardService
from src.card.forms import CardsFiltersForm

ROWS_PER_PAGE=10


class CardsController:

    def __init__(self):
        self.card_service = CardService()

    def cards(self):

        page = request.args.get('page', 1, type=int)
        filters = {}
        order = 'asc'
        field_sort = 'title'
        available_filters = ['set', 'color', 'mana', 'rarity', 'min_price', 'max_price', 'title']
        cards = self.card_service.get_cards(field_sort, order, filters, page, ROWS_PER_PAGE)
        form = CardsFiltersForm()
        if form.validate_on_submit():
            # handle form data
            pass
        return render_template('cards/cards_page.html', cards=cards, form=form)

    def create_card(self):
        data = request.get_json()
        card = Card(**data)
        self.card_service.add_card(card)
        return str(card), 201