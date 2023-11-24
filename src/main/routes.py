from flask import Blueprint

from src.main.controller import MainController

bp = Blueprint('main', __name__)

main_controller = MainController()
bp.add_url_rule('/', view_func=main_controller.root)