import api_easiedata
import sys
from src.easie import Easie
from src.spotify import Spotify
from src.utils import utils
from src.core import core



class EasieSync():
    """
        A class that is used to call core methods to syncronize data to easiedata 
        according to the defined project settings.
        
        Parameters
        ----------
        settings: dict
            {
                "easie": {
                    "user": "leo",
                    "developer_key": "f5a987e3e1c4e8de895c98a7e5b874ee",
                    "url_api": "http://127.0.0.1:5000"
                },
                "spotify": {
                    "client_id": "c15733ca83d240c2b1676a72d5c1454c",
                    "client_secret": "d24195c7580a40c18138b8273651f0a1"
                },
                "core": {
                    "artists_top_tracks":{
                        "names": [],
                        "top_tracks": 4,
                        "markets": []
                    },
                    "related_artists_top_tracks":{
                        "relative_popularity": 50,
                        "genres": [],
                        "top_tracks": 2,
                        "markets": []
                    },
                    "track_recomendations": {
                        "max_popularity": 100,
                        "seed_genres": [],
                        "seed_tracks_top": 5,
                        "markets": []
                    }
                }
            }
    """

    def __init__(self, settings):
        self.spotify = Spotify(**settings['spotify'])
        self.easie = Easie(**settings['easie'])
        self.core = settings['core']

    def __getitem__(self, k):
        return getattr(self, k)
    
    def get_artists_top_tracks(self):
        return core.artists_top_tracks(
            self.easie, self.spotify, **core['artists_top_tracks'])

    def get_related_artists_top_tracks(self):
        return core.related_artists_top_tracks(
            self.easie, self.spotify, **core['related_artists_top_tracks'])

    def get_track_recomendations(self):
        return core.track_recomendations(
            self.easie, self.spotify, **core['track_recomendations'])

    def get_all(self):
        self.get_artists_top_tracks()
        self.get_related_artists_top_tracks()
        self.get_track_recomendations()
        return self
     

if __name__ == '__main__':
    insertion_res = EasieSync(utils.get_settings())[sys.argv[2]]()
    utils.pretty_print(insertion_res)
    

