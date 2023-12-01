from flask import request, render_template, session, redirect, url_for
from src.models import Card

from src.card.card_service import CardService
from src.card.forms import CardsFiltersForm

ROWS_PER_PAGE=10


class CardsController:

    def __init__(self):
        self.card_service = CardService()

    def cards(self):
        form = CardsFiltersForm()

        if form.validate_on_submit():
            session['selected_set'] = request.form.get('set', "All")
            session['selected_color'] = request.form.get('color', "All")
            session['selected_mana'] = request.form.get('mana', "All")
            session['selected_rarity'] = request.form.get('rarity', "All")
            return redirect(url_for('card.cards'))

        page = request.args.get('page', 1, type=int)
        filters = {}
        selected_set = session.get('selected_set', "All")
        selected_color = session.get('selected_color', "All")
        selected_mana = session.get('selected_mana', "All")
        selected_rarity = session.get('selected_rarity', "All")

        if selected_set == "ALL":
            filters.pop("CardDetails.set", None)
        else:
            filters['CardDetails.set'] = selected_set

        if selected_color == "ALL":
            filters.pop("CardDetails.color", None)
        else:
            filters['CardDetails.color'] = selected_color

        if selected_mana == "ALL":
            filters.pop("CardDetails.mana", None)
        else:
            filters['CardDetails.mana'] = selected_mana

        if selected_rarity == "ALL":
            filters.pop("CardDetails.rarity", None)
        else:
            filters['CardDetails.rarity'] = selected_rarity

        form.set.data = selected_set
        form.color.data = selected_color
        form.mana.data = selected_mana
        form.rarity.data = selected_rarity

        order = 'asc'
        field_sort = 'title'
        cards = self.card_service.get_cards(field_sort, order, filters, page, ROWS_PER_PAGE)

        return render_template('cards/cards_page.html',
                               cards=cards,
                               form=form,
                               url_view="card.cards")

    def create_card(self):
        data = request.get_json()
        card = Card(**data)
        self.card_service.add_card(card)
        return str(card), 201