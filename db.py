# from contextlib import contextmanager
# import logging
# import os

# from flask import current_app, g

# import psycopg2
# from psycopg2.pool import ThreadedConnectionPool
# from psycopg2.extras import DictCursor

# pool = None

# def setup():
#     global pool
#     DATABASE_URL = os.environ['DATABASE_URL']
#     current_app.logger.info(f"creating db connection pool")
#     pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


# @contextmanager
# def get_db_connection():
#     try:
#         connection = pool.getconn()
#         yield connection
#     finally:
#         pool.putconn(connection)


# @contextmanager
# def get_db_cursor(commit=False):
#     with get_db_connection() as connection:
#       cursor = connection.cursor(cursor_factory=DictCursor)
#       # cursor = connection.cursor()
#       try:
#           yield cursor
#           if commit:
#               connection.commit()
#       finally:
#           cursor.close()

# # def get_login_info(username, password):
# #   with get_db_cursor(True) as cursor:
# #     cursor.execute("SELECT user_id FROM mixtape_fm_users WHERE username=%d, password=%d;", (username, password))
# #     return cursor.fetchall()

# # def attempt_registration(username, password):
# #   if (get_login_info(username, password) != None):
# #     return (False, None)
# #   with get_db_cursor(True) as cursor:
# #     cursor.execute("INSERT INTO mixtape_fm_users (username, password, spotify_linked) VALUES (%s, %s, %r);", (username, password, False))
# #   return (True, get_login_info(username, password))

# def get_playlist(playlist_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT * FROM mixtape_fm_playlists WHERE playlist_id=%s;", playlist_id)
#     return cursor.fetchall()

# def get_playlist_songs_ids(playlist_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT song_id FROM mixtape_fm_playlist_songs WHERE playlist_id=%s;", playlist_id)
#     return cursor.fetchall()

# def get_songs_from_song_id(song_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT * FROM mixtape_fm_songs WHERE song_id=%s;", song_id)
#     return cursor.fetchall()

# def get_playlist_songs(playlist_id):
#   playlist_songs_ids = get_playlist_songs_ids(playlist_id)
#   playlist_songs = []
#   for song_id in playlist_songs_ids:
#     playlist_songs.append(get_songs_from_song_id(song_id))
#   return playlist_songs

# def get_user_playlists(user_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT * FROM mixtape_fm_playlists WHERE user_id=%s;", user_id)
#     return cursor.fetchall()

# def get_playlist_id(user_id, playlist_name):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT playlist_id FROM mixtape_fm_playlists WHERE user_id=%s, playlist_name=%s;", (user_id, playlist_name))
#     return cursor.fetchall()

# def get_playlist_song_id(playlist_id, song_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT playlist_song_id FROM mixtape_fm_playlist_songs WHERE playlist_id=%s, song_id=%s;", (playlist_id, song_id))
#     return cursor.fetchall()

# def get_song_id(name, artist, album, genre, duration):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("SELECT song_id FROM mixtape_fm_songs WHERE name=%s, artist=%s, album=%s, genre=%s, duration=%s;", \
#     (name, artist, album, genre, duration))
#     return cursor.fetchall()

# def insert_playlist(user_id, playlist_name):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("INSERT INTO mixtape_fm_playlists (user_id, playlist_name, creation_date) VALUES (%s, %s, CURRENT_TIMESTAMP);", \
#     (user_id, playlist_name))
#     return get_playlist_id(user_id, playlist_name)

# def insert_song_into_playlist(playlist_id, song_id):
#   with get_db_cursor(True) as cursor:
#     cursor.execute("INSERT INTO mixtape_fm_playlist_songs (playlist_id, song_id) VALUES (%s, %s);", (playlist_id, song_id))
#     return get_playlist_song_id(playlist_id, song_id)

# def insert_song(name, artist, album, genre, duration):
#   if (get_song_id(name, artist, album, genre, duration) == None):
#     with get_db_cursor(True) as cursor:
#       cursor.execute("INSERT INTO mixtape_fm_songs (name, artist, album, genre, duration) VALUES (%s, %s, %s, %s, %s);", \
#       (name, artist, album, genre, duration))
#       return get_song_id(name, artist, album, genre, duration)