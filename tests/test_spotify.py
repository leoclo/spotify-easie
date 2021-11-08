import os
import pandas as pd
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.spotify import Spotify
from src.utils import utils


class TestSpotify(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spotify = Spotify.from_settings(utils.get_settings())

    def test_a_search_artists(self):
        """ Tests spotify.get_artists method """

        artists = ['coldplay', 'hdsafgahjsdg']
        artist_id = self.spotify.search_artist(artists[0])
        self.assertTrue('4gzpq5DPGxSnKTe4SA8HAU' == artist_id)
        self.assertRaises(ValueError, self.spotify.search_artist, artists[1])

    def test_b_related_artists(self):
        """ Tests spotify.get_related_artists method """

        artist_id = '4gzpq5DPGxSnKTe4SA8HAU'
        check_id =  '53A0W3U0s8diEn9RhXQhVz'
        rel_artists_ids = self.spotify.get_related_artists(artist_id)
        self.assertTrue(check_id in rel_artists_ids)

    def test_c_artists_basic_info(self):
        """ Tests spotify.get_artists_basic_info method """

        artists_id = ['4gzpq5DPGxSnKTe4SA8HAU', '53A0W3U0s8diEn9RhXQhVz']
        artists_info = self.spotify.get_artists_basic_info(artists_id)
        self.assertTrue(len(artists_info)==2)
        self.assertTrue('artist_followers_total' in artists_info[0])

    def test_d_artist_top_tracks_basic_info(self):
        """ Tests spotify.get_artist_top_tracks_basic_info method """

        artist_id = '4gzpq5DPGxSnKTe4SA8HAU'
        market = 'US'
        tracks_info = self.spotify.get_artist_top_tracks_basic_info(artist_id, market)
        self.assertTrue(len(tracks_info) > 0)
        self.assertTrue('track_album_id' in tracks_info[0])


    def test_e_get_recomendations_track_info(self):
        """ Tests spotify.get_recomendations_track_info method """

        q_params_exc = {
            'seed_artists': ['4gzpq5DPGxSnKTe4SA8HAU', '53A0W3U0s8diEn9RhXQhVz'],
            'seed_genres': ['pop']
        }
        self.assertRaises(ValueError, self.spotify.get_recomendations_track_info, q_params_exc)
        q_params = {
            'seed_artists': ['4gzpq5DPGxSnKTe4SA8HAU', '53A0W3U0s8diEn9RhXQhVz'],
            'seed_genres': ['pop'],
            'seed_tracks': ['46HNZY1i7O6jwTA7Slo2PI', '3AJwUDP919kvQ9QcozQPxg'],

        }

        tracks_info = self.spotify.get_recomendations_track_info(q_params)
        self.assertTrue(len(tracks_info) > 0)
        self.assertTrue('artists_ids' in tracks_info[0])











if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])