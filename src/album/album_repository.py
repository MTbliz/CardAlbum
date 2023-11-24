from src.models import Album
from src import db


class AlbumRepository:

    def get_albums(self):
        albums = Album.query.all()
        return albums

    def get_album(self, album_id):
        album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        return album

    def add_album(self, album: Album):
        db.session.add(album)
        db.session.commit()

    def delete_album(self, album_id):
        album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        db.session.delete(album)
        db.session.commit()
