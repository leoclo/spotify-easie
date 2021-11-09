import sys
from src.easie import Easie
from src.spotify import Spotify
from src.utils import utils
from src.core import core


class EasieSync():
    """
        A class that is used to call core methods according to the defined project settings.

        Parameters
        ----------
        settings: dict
    """

    def __init__(self, settings):
        self.spotify = Spotify(**settings['spotify'])
        self.easie = Easie(**settings['easie'])
        self.core_settings = settings['core']

    def __getitem__(self, k):
        return getattr(self, k)

    def build_artists_top_tracks(self):
        """ build artists_top_tracks table in easie"""

        return core.artists_top_tracks(
            self.easie,
            self.spotify,
            self.core_settings['artists_top_tracks'],
            self.core_settings['easie_table_ref']
        )

    def build_related_artists_top_tracks(self):
        """ build related_artists_top_tracks table in easie"""

        return core.related_artists_top_tracks(
            self.easie,
            self.spotify,
            self.core_settings['related_artists_top_tracks'],
            self.core_settings['easie_table_ref']
        )

    def build_track_recommendations(self):
        """ build track_recommendations table in easie"""

        return core.track_recommendations(
            self.easie,
            self.spotify,
            self.core_settings['track_recommendations'],
            self.core_settings['easie_table_ref']
        )

    def build_all(self):
        """ build all core tables in easie"""

        self.build_artists_top_tracks()
        self.build_related_artists_top_tracks()
        return self.build_track_recommendations()


if __name__ == '__main__':
    insertion_res = EasieSync(utils.get_settings())[sys.argv[2]]()
    utils.pretty_print(insertion_res)
