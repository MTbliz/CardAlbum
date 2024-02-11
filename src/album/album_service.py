from flask import abort
from flask_login import current_user
from loguru import logger

from src.album.album_repository import AlbumRepository
from src.models import Album


class AlbumService:

    def __init__(self) -> None:
        self.album_repository: AlbumRepository = AlbumRepository()

    def get_albums(self) -> list[Album]:
        logger.info("Retrieving all albums.")
        albums = self.album_repository.get_albums()
        logger.info(f"Retrieved albums.")
        return albums

    def get_album(self, album_id: int) -> Album:
        logger.info(f"Attempting to retrieve album with ID {album_id}.")
        album: Album = self.album_repository.get_album(album_id)
        if not album:
            logger.error(f"Album with ID {album_id} not found.")
            abort(404)
        elif current_user.id != album.user_id:
            logger.warning(f"User {current_user.id} tried to access album {album_id} owned by another user.")
            abort(403)
        else:
            logger.info(f"User {current_user.id} accessed album {album_id}.")
            return album

    # To correct. It should be searched by album_id, title can be duplicated between users.
    def get_album_cards(self, album_title: str, field_sort: str, order: str, filters: dict[str, str], page: int,
                        ROWS_PER_PAGE: int):
        logger.info("Retrieving album cards.")
        albums = self.album_repository.get_album_cards(album_title, field_sort, order, filters, page, ROWS_PER_PAGE)
        logger.info(f"Retrieved album cards.")
        return albums

    def add_album(self, album: Album) -> None:
        logger.info(f"Attempting to add album with ID {album.id}.")
        if current_user.id != album.user_id:
            logger.warning(f"User {current_user.id} tried to add album {album.id} owned by another user.")
            abort(403)
        else:
            logger.info(f"User {current_user.id} add album {album.id}.")
            self.album_repository.add_album(album)

    def delete_album(self, album_id: int) -> None:
        logger.info(f"Attempting to delete album with ID {album_id}.")
        album: Album = self.album_repository.get_album(album_id)
        if album is None:
            logger.error(f"Album with ID {album_id} not found.")
            abort(404)
        elif current_user.id != album.user_id:
            logger.warning(f"User {current_user.id} tried to delete album {album_id} owned by another user.")
            abort(403)
        else:
            self.album_repository.delete_album(album_id)
            logger.info(f"Successfully deleted album with ID {album_id}.")

    def get_albums_by_user(self, user_id: int) -> list[Album]:
        logger.info(f"Retrieving albums by user_card {user_id}.")
        if current_user.id != user_id:
            logger.warning(f"User {current_user.id} tried to access albums owned by another user.")
            abort(403)
        else:
            albums = self.album_repository.get_ablums_by_user(user_id)
            logger.info(f"User {current_user.id} accessed albums.")
            return albums

    def get_albums_by_user_card(self, card_id: int) -> list[Album]:
        logger.info(f"Retrieving albums by user_card {card_id}.")
        albums = self.album_repository.get_albums_by_user_card(card_id)
        if len(albums) > 0 and any(album.user_id != current_user.id for album in albums):
            logger.warning(f"User {current_user.id} tried to access albums owned by another user by user_card {card_id}")
            abort(403)
        else:
            logger.info(f"User {current_user.id} accessed albums.")
            return albums
