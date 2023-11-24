from src.album.album_repository import AlbumRepository


class AlbumService:

    def __init__(self):
        self.album_repository = AlbumRepository()

    def get_albums(self):
        return self.album_repository.get_albums()

    def get_album(self, album_id):
        return self.album_repository.get_album(album_id)

    def add_album(self, album):
        return self.album_repository.add_album(album)

    def delete_album(self, album_id):
        return self.album_repository.delete_album(album_id)