from flask import Blueprint

from src.album.album_controller import AlbumController

bp = Blueprint('album', __name__)

album_controller = AlbumController()
#bp.add_url_rule('/', view_func=album_controller.albums)
bp.add_url_rule('/<album_title>', view_func=album_controller.album_cards, methods=['GET', 'POST'])
bp.add_url_rule('/album', view_func=album_controller.create_album, methods=['POST'])
bp.add_url_rule('/<album_title>/<card_id>/<album_id>', view_func=album_controller.remove_user_card_from_album, methods=['GET'])