from flask import request, session, redirect, url_for, render_template
from src.models import Album

from src.album.album_forms import CreateAlbumForm, DeleteAlbumForm
from src.album.album_service import AlbumService
from src.card.user_card_service import UserCardService
from src.card.forms import CardsFiltersForm

ROWS_PER_PAGE = 10

class AlbumController:

    def __init__(self):
        self.album_service = AlbumService()
        self.user_card_service = UserCardService()

    def album_cards(self, album_title):

        form = CardsFiltersForm()

        if form.validate_on_submit():
            session['card_selected_set'] = request.form.get('set', "ALL")
            session['card_selected_color'] = request.form.get('color', "ALL")
            session['card_selected_mana'] = request.form.get('mana', "ALL")
            session['card_selected_rarity'] = request.form.get('rarity', "ALL")
            return redirect(url_for('album.album_cards', album_title=album_title))

        page = request.args.get('page', 1, type=int)
        filters = {}
        selected_set = session.get('card_selected_set', "ALL")
        selected_color = session.get('card_selected_color', "ALL")
        selected_mana = session.get('card_selected_mana', "ALL")
        selected_rarity = session.get('card_selected_rarity', "ALL")

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

        order = 'asc'
        field_sort = 'title'
        album_cards = self.album_service.get_album_cards(album_title, field_sort, order, filters, page, ROWS_PER_PAGE)

        return render_template('albums/album_page.html',
                               user_cards=album_cards,
                               form=form,
                               url_view="album.album_cards",
                               params={"album_title": album_title})

    def create_album(self):
        form = CreateAlbumForm()
        if form.validate_on_submit():
            album = Album()
            album.title = request.form['title']
            self.album_service.add_album(album)
            user_albums = session['user_albums']
            user_albums.append(album.title)
            session['user_albums'] = user_albums
        return render_template('albums/create_album_page.html', form=form)

    def delete_album(self):
        albums = self.album_service.get_albums_by_user('user_id')
        choices = [(album.id, album.title) for album in albums]
        form = DeleteAlbumForm()
        form.album.choices = choices
        if form.validate_on_submit():
            album_id = request.form.get('album')
            album = self.album_service.get_album(album_id)
            if album:
                self.album_service.delete_album(album_id)
                user_albums = session['user_albums']
                user_albums.remove(album.title)
                session['user_albums'] = user_albums
        return render_template('albums/delete_album_page.html', form=form)

    def remove_user_card_from_album(self, card_id, album_id, album_title):
        self.user_card_service.remove_user_card_from_album(card_id, album_id)
        return redirect(url_for('album.album_cards', album_title=album_title))