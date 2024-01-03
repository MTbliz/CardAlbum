from flask import render_template, session
from src.album.album_service import AlbumService


class MainController:

    def __init__(self):
        self.album_service = AlbumService()

    def root(self):
        user_albums = self.album_service.get_albums_by_user("user_id")
        session['user_albums'] = [user_album.title for user_album in user_albums]
        return render_template("base.html")





