import os
from typing import Union, Optional

from flask import request, render_template, session, redirect, url_for
from flask_login import current_user
from werkzeug.wrappers import Response

from src.album.album_service import AlbumService
from src.card.cardDTO import CardDTO, UserCardDTO
from src.card.card_service import CardService
from src.card.forms import CardsFiltersForm, CardSearchForm, CreateCardForm
from src.card.user_card_service import UserCardService
from src.models import Card, UserCard, Album

ROWS_PER_PAGE = 10


class CardsController:

    def __init__(self) -> None:
        self.card_service: CardService = CardService()
        self.user_card_service: UserCardService = UserCardService()
        self.album_service: AlbumService = AlbumService()

    def cards(self) -> str:
        form: CardsFiltersForm = CardsFiltersForm()

        if form.validate_on_submit():
            session['card_selected_set'] = request.form.get('set', "ALL")
            session['card_selected_color'] = request.form.get('color', "ALL")
            session['card_selected_mana'] = request.form.get('mana', "ALL")
            session['card_selected_rarity'] = request.form.get('rarity', "ALL")
            return redirect(url_for('card.cards'))

        page: int = request.args.get('page', 1, type=int)
        filters: dict = {}
        selected_set: str = session.get('card_selected_set', "ALL")
        selected_color: str = session.get('card_selected_color', "ALL")
        selected_mana: str = session.get('card_selected_mana', "ALL")
        selected_rarity: str = session.get('card_selected_rarity', "ALL")

        if selected_set == "ALL":
            filters.pop("CardDetails.set", None)
        else:
            filters['CardDetails.set'] = selected_set

        if selected_color == "ALL":
            filters.pop("CardDetails.colors", None)
        else:
            filters['CardDetails.colors'] = selected_color

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

        order: str = 'asc'
        field_sort: str = 'title'
        user_cards = self.user_card_service.get_cards(current_user.id, field_sort, order, filters, page, ROWS_PER_PAGE)

        user_albums: list[Album] = self.album_service.get_albums_by_user(current_user.id)
        cards_possible_albums: dict[Album] = {}
        for user_card in user_cards:
            card_albums: list[Album] = user_card.albums
            possible_albums = [album for album in user_albums if
                               album.id not in [card_album.id for card_album in card_albums]]
            cards_possible_albums[user_card.id] = possible_albums

        return render_template('cards/cards_page.html',
                               user_cards=user_cards,
                               cards_possible_albums=cards_possible_albums,
                               form=form,
                               url_view="card.cards",
                               params={})

    def create_card(self) -> Union[str, Response]:
        base_link: str = 'https://www.mtggoldfish.com/price'

        search_form: CardSearchForm = CardSearchForm()
        create_card_form: CreateCardForm = CreateCardForm()

        if search_form.validate_on_submit():
            session['card_searched_title'] = request.form.get('title', "")
            session['card_searched_set'] = request.form.get('set', "All")
            return redirect(url_for('card.create_card'))

        searched_title: str = session.get('card_searched_title', "")
        searched_set: str = session.get('card_searched_set', "All")

        search_form.title.data = searched_title
        search_form.set.data = searched_set

        card_image: str = 'img/img.jpg'
        if searched_title != "":

            if self.card_service.check_if_card_exist(searched_title):
                card: Card = self.card_service.get_card_by_title(searched_title)
            else:
                card: Card = self._save_or_get_card(base_link, searched_title, searched_set)  # Tu wrócić i poprawić
            if card:
                card_image: str = f"img/{searched_title}.jpg"
                create_card_form.title.data = searched_title
                create_card_form.set.data = self.card_service.get_set_value_by_name(searched_set)
                create_card_form.rarity.data = card.card_details.rarity.value
                create_card_form.mana.data = card.card_details.mana.value
                create_card_form.type.data = card.card_details.type
                create_card_form.color.data = ",".join(
                    [card_color.color.value for card_color in card.card_details.colors])

        if create_card_form.validate_on_submit():
            if not self.user_card_service.check_if_user_card_exists(card.id, current_user.id):
                user_card_dto: UserCardDTO = UserCardDTO(card,
                                                         create_card_form.price.data,
                                                         create_card_form.availability.data,
                                                         create_card_form.quality.data,
                                                         current_user.id)
                user_card: UserCard = user_card_dto.to_user_card()
                self.user_card_service.add_card(user_card)
            else:
                print("This card is in your collection.")

        return render_template('cards/create_card_page.html', form=search_form, create_card_form=create_card_form,
                               card_image=card_image)

    def _save_or_get_card(self, base_link: str, searched_title: str, searched_set: str) -> Optional[Card]:

        response: dict[str, any] = self.card_service.get_card_details_from_url(
            base_link,
            self.card_service.get_set_value_by_name(searched_set),
            searched_title)

        if response.get('status_code') == 200:
            card_details: dict[str, any] = response.get('body')
            if not os.path.exists(f'src/static/img/{searched_title}.jpg'):
                with open(f'src/static/img/{searched_title}.jpg', 'wb') as f:
                    f.write(card_details.get('img_data'))

            card_dto: CardDTO = CardDTO(searched_title,
                                        card_details.get('color').split(","),
                                        card_details.get('mana_cost'),
                                        card_details.get('rarity'),
                                        self.card_service.get_set_value_by_name(searched_set),
                                        card_details.get('type')
                                        )
            card: Card = card_dto.to_card()
            self.card_service.add_card(card)
        else:
            card = None
        return card

    def store_or_clear_endpoint(self) -> None:
        if session.get('previous_endpoint') != request.endpoint:
            for key in list(session.keys()):
                if key.startswith('card_'):
                    session.pop(key)
        session['previous_endpoint'] = request.endpoint

    def delete_user_card(self, id: int) -> Response:
        self.user_card_service.delete_card(id)
        return redirect(url_for('card.cards'))

    def remove_user_card_from_album(self, card_id: int, album_id: int) -> Response:
        self.user_card_service.remove_user_card_from_album(card_id, album_id)
        return redirect(url_for('card.cards'))

    def add_user_card_to_album(self, card_id: int, album_id: int) -> Response:
        self.user_card_service.add_user_card_to_album(card_id, album_id)
        return redirect(url_for('card.cards'))
