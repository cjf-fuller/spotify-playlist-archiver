import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# SPOTIFY APP SECRETS & CONFIG
cid = '<SPOTIFY-APP-ID>'
secret = '<SPOTIFY-APP-SECRET>'
scope = 'playlist-modify-private'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# SPOTIFY COLLABORATIVE PLAYLIST IDS

## example playlist 1
example1_pl_id = 'spotify:playlist:<PLAYLIST-ID>'
example1_pl_archive_id = 'spotify:playlist:<ARCHIVE-PLAYLIST-ID>'
example1_pl_limit = 75

## example playlist 2
example2_pl_id = 'spotify:playlist:<PLAYLIST-ID>'
example2_pl_archive_id = 'spotify:playlist:<ARCHIVE-PLAYLIST-ID>'
example2_pl_limit = 100

# ARCHIVER FUNCTION

def archiver(pl_id, pl_archive_id, pl_limit):
    response = sp.playlist_items(pl_id, offset=0, fields='items.track.uri')
    if len(response['items']) > pl_limit:
        diff = len(response['items']) - pl_limit
        spo = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=cid, client_secret=secret, redirect_uri='http://127.0.0.1:10888'))
        for track in range(diff):
            spo.playlist_add_items(pl_archive_id, [response['items'][track]['track']['uri']])
            spo.playlist_remove_all_occurrences_of_items(pl_id, [response['items'][track]['track']['uri']])

# EXECUTE ARCHIVER

archiver(example1_pl_id, example1_pl_archive_id, example1_pl_limit)
archiver(example2_pl_id, example2_pl_archive_id, example2_pl_limit)