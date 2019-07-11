import logging

from flask import Blueprint, jsonify, current_app

from src.db import Song, Session


bp = Blueprint("updater", __name__)


@bp.route('/')
def index():
    return jsonify(
        _api_version='1.0',
        _spotify_token=current_app.spotify._access_token is not None
    )


@bp.route('/scrap', methods=['GET'])
def scrap():
    song_history = current_app.scraper.get_song_history()

    return jsonify(song_history)


@bp.route('/update_playlist', methods=['POST'])
def update_playlist():
    # get song history
    song_history = current_app.scraper.get_song_history()

    # search for track in spotify
    spotify_songs = [current_app.spotify.search_track(s['title'], s['artist'])
                     for s in song_history if 'title' in s]

    valid_songs = [s for s in spotify_songs if 'spotify_uri' in s]

    # save tracks in DB
    session = Session()
    for song in valid_songs:
        session.add(Song(**song))
    session.commit()

    logging.info('will add {0} tracks'.format(len(valid_songs)))

    # add tracks to playlist
    response = current_app.spotify.add_tracks_to_playlist(
        [s['spotify_uri'] for s in valid_songs]
    )

    return jsonify(**response)
