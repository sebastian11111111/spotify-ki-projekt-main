from typing import Any, Dict

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify:

    def __init__(self):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id='2b9bc1b0cb0c42278019aba8fd26d7df',
                                                                client_secret='639bc38548a741a68c63f0c4746f6a90'))
        self.errors = []

    def get_artist(self, name: str):
        try:
            search_results = self.spotify.search(name, 1, 0, "artist")
            artist = search_results['artists']['items'][0]
            return artist
        except IndexError as e:
            self.errors.append(name)
            return {'name': name, 'popularity': 0, 'followers': {'total': 0}}
