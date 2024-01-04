from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField


class CreateAlbumForm(FlaskForm):
    title = StringField('Title:')
    submit = SubmitField('Create Album')


class DeleteAlbumForm(FlaskForm):
    album = SelectField('Album:')
    submit = SubmitField('Delete Album')
