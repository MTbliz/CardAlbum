from flask import request, render_template, session, redirect, url_for
import os

from src.card.cardDTO import CardDTO
from src.card.card_service import CardService
from src.card.forms import CardsFiltersForm, CardSearchForm, CreateCardForm


ROWS_PER_PAGE = 10


class CardsController:

    def __init__(self):
        self.card_service = CardService()

    def cards(self):
        form = CardsFiltersForm()

        if form.validate_on_submit():
            session['card_selected_set'] = request.form.get('set', "All")
            session['card_selected_color'] = request.form.get('color', "All")
            session['card_selected_mana'] = request.form.get('mana', "All")
            session['card_selected_rarity'] = request.form.get('rarity', "All")
            return redirect(url_for('card.cards'))

        page = request.args.get('page', 1, type=int)
        filters = {}
        selected_set = session.get('card_selected_set', "All")
        selected_color = session.get('card_selected_color', "All")
        selected_mana = session.get('card_selected_mana', "All")
        selected_rarity = session.get('card_selected_rarity', "All")

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
        base_link = 'https://www.mtggoldfish.com/price'

        search_form = CardSearchForm()
        create_card_form = CreateCardForm()

        if search_form.validate_on_submit():
            session['card_searched_title'] = request.form.get('title', "")
            session['card_searched_set'] = request.form.get('set', "All")
            return redirect(url_for('card.create_card'))

        searched_title = session.get('card_searched_title', "")
        searched_set = session.get('card_searched_set', "All")

        search_form.title.data = searched_title
        search_form.set.data = searched_set

        card_image = 'img/img.jpg'
        if searched_title != "":
            resposne = self.card_service.get_card_details_from_url(base_link, self.card_service.get_set_value_by_name(searched_set), searched_title)
            if resposne.get('status_code') == 200:
                card_details = resposne.get('body')
                if not os.path.exists(f'src/static/img/{searched_title}.jpg'):
                    with open(f'src/static/img/{searched_title}.jpg', 'wb') as f:
                        f.write(card_details.get('img_data'))
                card_image = f"img/{searched_title}.jpg"

                create_card_form.title.data = searched_title
                create_card_form.set.data = self.card_service.get_set_value_by_name(searched_set)
                create_card_form.rarity.data = card_details.get('rarity')
                create_card_form.mana.data = card_details.get('mana_cost')
                create_card_form.type.data = card_details.get('type')
                create_card_form.color.data = card_details.get('color')

        if create_card_form.validate_on_submit():
            card_title = create_card_form.title.data
            card_color_str = create_card_form.color.data
            card_mana_str = create_card_form.mana.data
            card_rarity_str = create_card_form.rarity.data
            card_set_str = create_card_form.set.data
            card_type = create_card_form.type.data
            card_quality = create_card_form.quality.data
            card_price = create_card_form.price.data
            card_availability = create_card_form.availability.data
            card_dto = CardDTO(card_title,
                               card_color_str,
                               card_mana_str,
                               card_rarity_str,
                               card_set_str,
                               card_type,
                               card_quality,
                               card_price,
                               card_availability)
            card = card_dto.to_card()
            self.card_service.add_card(card)

        return render_template('cards/create_card_page.html', form=search_form, create_card_form=create_card_form, card_image=card_image)

    def store_or_clear_endpoint(self):
        if session.get('previous_endpoint') != request.endpoint:
            for key in list(session.keys()):
                if key.startswith('card_'):
                    session.pop(key)
        session['previous_endpoint'] = request.endpoint