from flask import Flask
from src.extensions import db
from configuration import DevConfig
from src.main.routes import bp as main_bp
from src.album.album_routes import bp as album_bp
from src.card.card_routes import bp as card_bp


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(album_bp, url_prefix='/albums')
    app.register_blueprint(card_bp, url_prefix='/cards')
    return app
