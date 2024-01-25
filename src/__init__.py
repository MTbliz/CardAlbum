from flask import Flask
from src.extensions import db, login_manager

from configuration import DevConfig
from src.album.album_routes import bp as album_bp
from src.basket.basket_routes import bp as basket_bp
from src.card.card_routes import bp as card_bp
from src.main.routes import bp as main_bp
from src.order.order_routes import bp as order_bp


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(album_bp, url_prefix='/albums')
    app.register_blueprint(card_bp, url_prefix='/cards')
    app.register_blueprint(basket_bp, url_prefix='/basket')
    app.register_blueprint(order_bp, url_prefix='/orders')
    return app
