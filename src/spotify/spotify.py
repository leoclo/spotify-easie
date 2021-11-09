import requests


class Spotify():
    """
        A class that is used to retrieve data from spotify"
        Reference:
        https://developer.spotify.com/documentation/web-api/reference/#/

        Parameters
        ----------

        client_id : str
            spotify developer id
        client_secret : str
            client generated key
        track_info: list
            list with keys to be fetched from spotify track object
        artist_info: list
            list with keys to be fetched from spotify artist_info object
    """

    def __init__(self, client_id, client_secret, track_info, artist_info):
        self.client_id = client_id
        self.client_secret = client_secret
        self.track_info = track_info
        self.artist_info = artist_info

        res = requests.post(
            'https://accounts.spotify.com/api/token',
            auth=(self.client_id, self.client_secret),
            data={'grant_type': 'client_credentials'}
        )
        self.headers = {
            'Authorization': f"Bearer {res.json()['access_token']}"
        }

    @classmethod
    def from_settings(cls, settings):
        return cls(**settings['spotify'])

    @property
    def track_info(self):
        return self._track_info

    @track_info.setter
    def track_info(self, value):
        required_info = ['id', 'name', 'popularity', 'album.release_date']
        self._track_info = list(set(value + required_info))

    @property
    def artist_info(self):
        return self._artist_info

    @artist_info.setter
    def artist_info(self, value):
        required_info = ['id', 'name', 'popularity', 'followers.total']
        self._artist_info = list(set(value + required_info))

    def _get(self, url):
        """ Method to perform get request to api.spotify.com/v1/ """

        return requests.get(
            'https://api.spotify.com/v1/' + url, headers=self.headers
        ).json()

    def _get_res_key(self, d, keys):
        """ Method to recursively get keys inside dictionary """

        if len(keys) > 1:
            return self._get_res_key(d[keys[0]], keys[1:])
        if isinstance(d[keys[0]], list):
            return ' / '.join(d[keys[0]])
        return d[keys[0]]

    def _get_res_info(self, d, infos, info_type):
        """ Method to get spotify response focus info """
        return  {
            f"{info_type}_{i.replace('.', '_')}": self._get_res_key(d, i.split('.'))
            for i in infos
        }

    def search_artist(self, artist_name):
        """ Method to retrieve artist_id by name """

        res = self._get(f'search?type=artist&q={artist_name}&limit=1')

        if len(res['artists']['items']) == 0:
            raise ValueError(f'Artist "{artist_name}" not found')

        return res['artists']['items'][0]['id']

    def get_related_artists(self, artist_id):
        """ Method to retrieve related artists ids"""

        res = self._get(f'artists/{artist_id}/related-artists')
        return [a['id'] for a in res['artists']]

    def get_artists_info(self, artist_ids):
        """ Method to retrieve several artist's basic information """

        res = self._get(f"artists/?ids={','.join(artist_ids)}")
        return [
            self._get_res_info(a, self.artist_info, 'artist')
            for a in res['artists']
        ]

    def get_artist_top_tracks_info(self, artist_id, market=''):
        """
            Method to retrieve basic info from most popular tracks from an
            artist
        """

        url = f'artists/{artist_id}/top-tracks'
        if market:
            url += f'?market={market}'

        res = self._get(url)
        return [
            self._get_res_info(t, self.track_info, 'track')
            for t in res['tracks']
        ]

    def get_recomendations_track_info(self, q_params):
        """
            Method to retrieve track recommendations info

            Refer to:
            #https://developer.spotify.com/documentation/web-api/
            reference/#/operations/get-recommendations
        """

        list_params = ['seed_artists', 'seed_genres', 'seed_tracks']
        seed_size = 0
        for v in list_params:
            if v in q_params:
                seed_size += len(q_params[v])
                q_params[v] = ','.join(q_params[v])

        if seed_size != 5:
            raise ValueError(
                """
                q_params requires added lengths of seed_tracks, seed_genres
                and seed_artists to be greater than 4
                """
            )

        url = 'recommendations?' + '&'.join([
            f'{k}={v}' for k, v in q_params.items()
        ])

        res = self._get(url)['tracks']
        tracks = []

        for t in res:
            artists_ids = []
            artists_names = []
            for a in t['artists']:
                artists_ids.append(a['id'])
                artists_names.append(a['name'])

            tracks.append({
                'artists_ids': ' / '.join(artists_ids),
                'artists_names': ' / '.join(artists_names),
                **self._get_res_info(t, self.track_info, 'track')
            })

        return tracks
