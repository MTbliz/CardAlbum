from flask import request
from src.models import Album

from src.album.album_service import AlbumService


class AlbumController:

    def __init__(self):
        self.album_service = AlbumService()

    def albums(self):
        albums = self.album_service.get_albums()
        return str(albums)

    def create_album(self):
        data = request.get_json()
        album = Album(**data)
        self.album_service.add_album(album)
        return str(album), 201