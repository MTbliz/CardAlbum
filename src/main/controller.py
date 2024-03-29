from typing import Union

from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from loguru import logger
from werkzeug.wrappers import Response

from src import db
from src.album.album_service import AlbumService
from src.basket.basket_service import BasketService
from src.models import User, Album
from src.user.user_service import UserService


class MainController:

    def __init__(self) -> None:
        self.album_service: AlbumService = AlbumService()
        self.basket_service: BasketService = BasketService()
        self.user_service: UserService = UserService()

    def root(self) -> Union[str, Response]:
        logger.info("Root page accessed.")
        if current_user.is_authenticated:
            user_albums: list[Album] = self.album_service.get_albums_by_user(current_user.id)
            session['user_albums'] = [user_album.title for user_album in user_albums]

            basket_count: int = self.basket_service.get_basket_items_count(current_user.id)
            if basket_count is None:
                basket_count = 0
            session['basket_count'] = basket_count
            logger.info(f"Authenticated user {current_user.id} visited the root page.")
            return render_template("base.html")
        else:
            logger.info("Unauthenticated user attempted to visit the root page.")
            return redirect(url_for('main.login'))

    def login(self) -> Union[str, Response]:
        if request.method == 'POST':
            email: str = request.form.get('email')
            password: str = request.form.get('password')
            user: User = self.user_service.get_user_by_email(email)
            if user and user.check_password(password):
                login_user(user)
                logger.info(f"User {email} logged in successfully.")
                return redirect(url_for('main.root'))
            else:
                logger.warning(f"Failed login attempt for user {email}.")
                flash('Please check your login details and try again.', 'danger')
                return redirect(url_for('main.login'))
        return render_template('login.html')

    def logout(self) -> Response:
        user_id = current_user.id
        logout_user()
        logger.info(f"User {user_id} logged out successfully.")
        flash('Logged out successfully.', 'success')
        return redirect(url_for('main.login'))

    def signup(self) -> Union[str, Response]:
        if request.method == 'POST':
            email: str = request.form.get('email')
            username: str = request.form.get('username')
            password: str = request.form.get('password')

            user: User = self.user_service.get_user_by_email(email)

            if user:  # if a user is found, we want to redirect back to signup page so user can try again
                logger.warning(f"Signup attempt with existing email address: {email}")
                flash('Email address already exists', category='danger')
                return redirect(url_for('main.signup'))

            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user: User = User(email=email, username=username)
            new_user.set_password(password)

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            logger.info(f"New user {username} signed up successfully.")
            return redirect(url_for('main.login'))
        return render_template('signup.html')

    def profile(self) -> str:
        logger.info(f"Profile page accessed by user {current_user.id}.")
        return render_template('order.html')
