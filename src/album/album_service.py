from flask import abort
from flask_login import current_user

from src.album.album_repository import AlbumRepository
from src.models import Album


class AlbumService:

    def __init__(self) -> None:
        self.album_repository: AlbumRepository = AlbumRepository()

    def get_albums(self) -> list[Album]:
        return self.album_repository.get_albums()

    def get_album(self, album_id: int) -> Album:
        album: Album = self.album_repository.get_album(album_id)
        if not album:
            abort(404)
        elif current_user.id != album.user_id:
            abort(403)
        else:
            return album

    # To correct. It should be searched by album_id, title can be duplicated between users.
    def get_album_cards(self, album_title: str, field_sort: str, order: str, filters: dict[str, str], page: int,
                        ROWS_PER_PAGE: int):
        return self.album_repository.get_album_cards(album_title, field_sort, order, filters, page, ROWS_PER_PAGE)

    def add_album(self, album: Album) -> None:
        if current_user.id != album.user_id:
            abort(403)
        else:
            self.album_repository.add_album(album)

    def delete_album(self, album_id: int) -> None:
        album: Album = self.album_repository.get_album(album_id)
        if album is None:
            abort(404)
        elif current_user.id != album.user_id:
            abort(403)
        else:
            self.album_repository.delete_album(album_id)

    def get_albums_by_user(self, user_id: int) -> list[Album]:
        if current_user.id != user_id:
            abort(403)
        else:
            return self.album_repository.get_ablums_by_user(user_id)

    def get_albums_by_user_card(self, card_id: int) -> list[Album]:
        albums = self.album_repository.get_albums_by_user_card(card_id)
        if len(albums) > 0 and current_user.id != albums[0].user_id:
            abort(403)
        else:
            return albums
