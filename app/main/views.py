import app
from flask import render_template, request, flash, redirect, url_for, abort, \
    current_app
from flask_login import login_required, current_user
from . import main
from .forms import AddNewAlbumForm, EditAlbumForm
from .. import db
from ..models import Albums


@main.route('/account')
@login_required
def account():
    if request.method == 'GET':
        user = current_user
        return render_template('pages/account.html', user=user), 200


@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def home():
    return render_template('pages/home.html'), 200


@main.route('/biography', methods=['GET'])
def biography():
    return render_template('pages/biography.html'), 200


@main.route('/albums', methods=['GET'])
def albums():
    all_albums = db.session.query(Albums).all()
    return render_template('pages/albums.html', albums=all_albums,
                           user=current_user), 200


@main.route('/albums/new', methods=['GET', 'POST'])
@login_required
def add_new_album():
    form = AddNewAlbumForm()

    if request.method == 'GET':
        return render_template('pages/add_new_album.html', form=form), 200

    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            new_album = Albums(name=form.name.data,
                               released=form.released.data,
                               genres=form.genres.data,
                               description=form.description.data,
                               text=form.text.data,
                               language=form.language.data,
                               creator_id=user.id)

            db.session.add(new_album)
            db.session.commit()
            flash(message='Album was successfuly added.', category='info')

            photo = request.files['photo']
            filename = str(new_album.id) + '.jpg'
            photo.save(current_app.config['ALBUMS_PHOTOS_PATH'] + filename)

            return redirect(url_for('main.albums'))
        else:
            return render_template('pages/add_new_album.html', form=form), 200


@main.route('/albums/delete_album/<album_id>', methods=['GET'])
@login_required
def delete_album(album_id):
    album = db.session.query(Albums).filter_by(id=album_id).first()

    if album.creator_id == current_user.id:
        db.session.delete(album)
        db.session.commit()
        flash(f'{album.name} was successfuly deleted!', category='info')
    else:
        flash(f'{album.name} did not deleted, you do not have access!',
              category='warning')
    return redirect(url_for('main.albums'))


@main.route('/albums/edit/<album_id>', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    album = db.session.query(Albums).filter_by(id=album_id).first()

    if album is not None and current_user.id == album.creator_id:
        form = EditAlbumForm(name=album.name,
                             released=album.released,
                             genres=album.genres,
                             description=album.description,
                             text=album.text,
                             language=album.language)

        if request.method == 'GET':
            return render_template('pages/edit_album.html', form=form)

        if request.method == 'POST':
            if form.validate_on_submit():
                db.session.query(Albums).filter_by(id=album_id).update({
                    Albums.name: form.name.data,
                    Albums.released: form.released.data,
                    Albums.genres: form.genres.data,
                    Albums.description: form.description.data,
                    Albums.text: form.text.data,
                    Albums.language: form.language.data,
                })
                db.session.commit()
                flash(message='Album was successfuly edited.', category='info')
                return redirect(url_for('main.albums'))
            else:
                return render_template('pages/edit_album.html', form=form), 200
    else:
        return abort(404)


@main.route('/albums/album/<album_id>', methods=['GET'])
def show_album(album_id):
    album = db.session.query(Albums).filter_by(id=album_id).first()
    return render_template('pages/album.html', album=album), 200
