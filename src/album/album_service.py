from src.album.album_repository import AlbumRepository
from src.models import Album


class AlbumService:

    def __init__(self) -> None:
        self.album_repository: AlbumRepository = AlbumRepository()

    def get_albums(self) -> list[Album]:
        return self.album_repository.get_albums()

    def get_album(self, album_id: int) -> Album:
        return self.album_repository.get_album(album_id)

    def get_album_cards(self, album_title: str, field_sort: str, order: str, filters: dict[str, str], page: int,
                        ROWS_PER_PAGE: int):
        return self.album_repository.get_album_cards(album_title, field_sort, order, filters, page, ROWS_PER_PAGE)

    def add_album(self, album: Album) -> None:
        self.album_repository.add_album(album)

    def delete_album(self, album_id: int) -> None:
        self.album_repository.delete_album(album_id)

    def get_albums_by_user(self, user_id: int) -> list[Album]:
        return self.album_repository.get_ablums_by_user(user_id)

    def get_albums_by_user_card(self, card_id: int) -> list[Album]:
        return self.album_repository.get_albums_by_user_card(card_id)
