import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# SPOTIFY APP SECRETS & CONFIG
cid = os.environ.get('SPOTIFY_APP_ID')
secret = os.environ.get('SPOTIFY_APP_SECRET')
scope = 'playlist-modify-private'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# SPOTIFY COLLABORATIVE PLAYLIST IDS

## playlist 1
pl1_id = f"spotify:playlist:{os.environ.get('PLAYLIST_1_ID')}"
pl1_archive_id = f"spotify:playlist:{os.environ.get('ARCHIVE_PLAYLIST_1_ID')}"
pl1_limit = 75

## playlist 2
pl2_id = f"spotify:playlist:{os.environ.get('PLAYLIST_2_ID')}"
pl2_archive_id = f"spotify:playlist:{os.environ.get('ARCHIVE_PLAYLIST_2_ID')}"
pl2_limit = 90

## playlist 2
pl3_id = f"spotify:playlist:{os.environ.get('PLAYLIST_3_ID')}"
pl3_archive_id = f"spotify:playlist:{os.environ.get('ARCHIVE_PLAYLIST_3_ID')}"
pl3_limit = 90

def archiver(pl_id, pl_archive_id, pl_limit):
    """ archiver function """
    response = sp.playlist_items(pl_id, offset=0, fields='items.track.uri')
    print(len(response['items']))
    if len(response['items']) > pl_limit:
        diff = len(response['items']) - pl_limit
        spo = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret, redirect_uri='http://127.0.0.1:10888'))
        for track in range(diff):
            spo.playlist_add_items(pl_archive_id, [response['items'][track]['track']['uri']])
            spo.playlist_remove_all_occurrences_of_items(pl_id, [response['items'][track]['track']['uri']])


def lambda_handler(event=None, context=None):
    """ main Lambda event handling loop """

    print("Begin Archiver")
    archiver(pl1_id, pl1_archive_id, pl1_limit)
    print("Archive #1 Complete")
    archiver(pl2_id, pl2_archive_id, pl2_limit)
    print("Archive #2 Complete")
    archiver(pl3_id, pl3_archive_id, pl3_limit)
    print("Archive #3 Complete")
    print("All Done!")