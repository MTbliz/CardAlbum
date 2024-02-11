from flask import Blueprint

from src.album.album_controller import AlbumController

bp = Blueprint('album', __name__)

album_controller = AlbumController()
bp.add_url_rule('/<album_title>', view_func=album_controller.album_cards, methods=['GET', 'POST'])
bp.add_url_rule('/album', view_func=album_controller.create_album, methods=['GET', 'POST'])
bp.add_url_rule('/album/delete', view_func=album_controller.delete_album, methods=['GET', 'POST'])
bp.add_url_rule('/card/<card_id>/increase', view_func=album_controller.increase_user_card_availability, methods=['POST'])
bp.add_url_rule('/card/<card_id>/decrease', view_func=album_controller.decrease_user_card_availability, methods=['POST'])
bp.add_url_rule('/<album_title>/<card_id>/<album_id>', view_func=album_controller.remove_user_card_from_album,
                methods=['GET'])
