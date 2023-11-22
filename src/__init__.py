from flask import Flask
from src.extensions import db
from configuration import DevConfig
from src.main import bp as main_bp
from src.main.controller import CardsController


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints here
    cards_controller = CardsController()
    main_bp.add_url_rule('/', view_func=cards_controller.cards)
    main_bp.add_url_rule('/card', view_func=cards_controller.create_card, methods=['POST'])

    app.register_blueprint(main_bp)
    return app
