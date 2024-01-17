from flask import Blueprint

from src.main.controller import MainController

bp = Blueprint('main', __name__)

main_controller = MainController()
bp.add_url_rule('/', view_func=main_controller.root)
bp.add_url_rule('/login', view_func=main_controller.login, methods=['GET', 'POST'])
bp.add_url_rule('/logout', view_func=main_controller.logout, methods=['GET', 'POST'])
bp.add_url_rule('/profile', view_func=main_controller.profile)
bp.add_url_rule('/signup', view_func=main_controller.signup, methods=['GET', 'POST'])