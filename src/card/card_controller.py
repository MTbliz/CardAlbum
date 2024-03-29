from typing import Union

from flask import request, render_template, session, redirect, url_for, jsonify
from flask_login import current_user, login_required
from loguru import logger
from werkzeug.wrappers import Response

from src.album.album_service import AlbumService
from src.card.cardDTO import UserCardDTO
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

    @login_required
    def cards(self) -> str:
        logger.info(f"Visiting cards page.")
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

    @login_required
    def create_card(self) -> Union[str, Response]:
        logger.info(f"Create card page accessed by user: {current_user.username}")
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
            set_value: str = self.card_service.get_set_value_by_name(searched_set)

            if self.card_service.check_if_card_exist(searched_title, searched_set):
                card: Card = self.card_service.get_card_by_title(searched_title)
            elif self.card_service.is_card_title_available(searched_title):
                card: Card = None
            else:
                response = self.card_service.get_card_data_from_url(base_link, set_value, searched_title)
                if response.get('status_code') == 200:
                    card_details: dict[str, any] = response.get('body')
                    self.card_service.save_card(searched_title, set_value, card_details)
                    card: Card = self.card_service.get_card_by_title(searched_title)
                else:
                    card: Card = None
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
                logger.info(f"Card '{card.title}' added by user: {current_user.username} to collection.")
            else:
                logger.info(f"Card '{card.title}' in user: {current_user.username} collection.")

        return render_template('cards/create_card_page.html', form=search_form, create_card_form=create_card_form,
                               card_image=card_image)

    def store_or_clear_endpoint(self) -> None:
        if session.get('previous_endpoint') != request.endpoint:
            for key in list(session.keys()):
                if key.startswith('card_'):
                    session.pop(key)
        session['previous_endpoint'] = request.endpoint

    def delete_user_card(self, id: int) -> Response:
        logger.info(f"Deleting user card with ID {id}.")
        self.user_card_service.delete_card(id)
        logger.info(f"User card '{id}' deleted by user: {current_user.username}")
        return redirect(url_for('card.cards'))

    @login_required
    def remove_user_card_from_album(self, card_id: int, album_id: int) -> Response:
        logger.info(f"Removing user card with ID {card_id} from album {album_id}.")
        self.user_card_service.remove_user_card_from_album(card_id, album_id)
        logger.info(f"User card '{card_id}' deleted by user: {current_user.username} from album: {album_id}")
        return redirect(url_for('card.cards'))

    @login_required
    def add_user_card_to_album(self, card_id: int, album_id: int) -> Response:
        logger.info(f"Adding user card with ID {card_id} to album {album_id}.")
        self.user_card_service.add_user_card_to_album(card_id, album_id)
        logger.info(f"User card '{card_id}' added by user: {current_user.username} to album: {album_id}")
        return redirect(url_for('card.cards'))

    @login_required
    def increase_user_card_availability(self, card_id: int) -> Response:
        new_availability = self.user_card_service.increase_user_card_availability(card_id)
        return jsonify({"new_availability": new_availability}), 200

    @login_required
    def decrease_user_card_availability(self, card_id: int) -> Response:
        new_availability = self.user_card_service.decrease_user_card_availability(card_id)
        return jsonify({"new_availability": new_availability}), 200
