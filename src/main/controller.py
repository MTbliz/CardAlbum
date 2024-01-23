from flask import render_template, session, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, current_user
from sqlalchemy import func

from src.album.album_service import AlbumService
from src.basket.basket_service import BasketService
from src.models import User, Basket, BasketItem
from src import db


class MainController:

    def __init__(self):
        self.album_service = AlbumService()
        self.basket_service = BasketService()

    def root(self):
        if current_user.is_authenticated:
            user_albums = self.album_service.get_albums_by_user(current_user.id)
            session['user_albums'] = [user_album.title for user_album in user_albums]

            basket_count = BasketItem.query.join(Basket).filter(Basket.user_id==current_user.id).with_entities(func.sum(BasketItem.quantity)).scalar()
            if basket_count is None:
                basket_count = 0
            session['basket_count'] = basket_count
            return render_template("base.html")
        else:
            return redirect(url_for('main.login'))

    def login(self):
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('main.root'))
            else:
                flash('Please check your login details and try again.', 'danger')
                return redirect(url_for('main.login'))
        return render_template('login.html')

    def logout(self):
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('main.login'))

    def signup(self):
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user:  # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address already exists', category='danger')
                return redirect(url_for('main.signup'))

            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=email, username=username)
            new_user.set_password(password)

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('main.login'))
        return render_template('signup.html')

    def profile(self):
        return render_template('order.html')






