from src.utils import utils
import requests


class Spotify():

    def __init__(self):
        settings = utils.get_settings()
        self.client_id = settings['spotify']['client_id']
        self.client_secret = settings['spotify']['client_secret']

        url = 'https://accounts.spotify.com/api/token'
        res = requests.post(
            url, 
            auth=(self.client_id, self.client_secret),
            data={'grant_type': 'client_credentials'}
        )

        self.access_token = res.json()['access_token']
        return None

    def get_artists(self):
        return self

    def get_artists_top_songs(self):
        return self

    def merge(self):
        return self




        