from functools import wraps
import random
import pandas as pd
from . import data_manipulation


def easie_insertion(func):
    """ Decorator to insert in easiedata data assemble in the function """

    @wraps(func)
    def core_method(*args, **kwargs):
        easie, df_params = func(*args, **kwargs)
        easie.post_in_easie(df_params)
        return easie.post_res

    return core_method


@easie_insertion
def artists_top_tracks(easie, spotify, core_settings, easie_table_ref):
    """
        Consolidates spotify artists top n tracks  for insertion in easie

        Parameters
        ----------
        easie: Easie
            Easie instance
        spotify:
            Spotify instance
        core_settings: dict
            artists_names: list
                Names of artists to fetch top songs
            top_tracks: int
                N most popular songs to be considered
            markets: list
                markets to average song popularity
            easie_table_name: str
                Name of table in easiedata
        easie_table_ref: dict
            key is the name of the core function and value the name of the
            table on easiedata

    """

    artists_ids = [
        spotify.search_artist(a) for a in core_settings['artists_names']
    ]
    df = pd.DataFrame(spotify.get_artists_info(artists_ids))
    top_tracks = []
    for artist_id in artists_ids:
        for market in core_settings['markets']:
            top_tracks += [
                {
                    'artist_id': artist_id,
                    'market': market,
                    **t
                }
                for t in spotify.get_artist_top_tracks_info(artist_id, market)
            ]

    df = pd.DataFrame(top_tracks).merge(df, how='left', on='artist_id')

    df_params = [{
        'table_name': easie_table_ref['artists_top_tracks'],
        'action': 'insert_with_df',
        'df': data_manipulation.sort_n_largest_market_popularity(
            artists_ids, df, core_settings),
        'params': {'not_exists_create': True, 'replace': True}
    }]
    return easie, df_params



@easie_insertion
def related_artists_top_tracks(easie, spotify, core_settings, easie_table_ref):
    """
    Consolidates spotify related artists track data for insertion in easie

    Parameters
    ----------
    easie: Easie
        Easie instance
    spotify: Spotify
        Spotify instance
    core_settings: dict
        max_popularity: int
            Max popularity of related artists
        top_tracks: int
            N most popular songs to be considered
        markets: list
            markets to average song popularity
        easie_table_name: str
            Name of table in easiedata
    easie_table_ref: dict
        key is the name of the core function and value the name of the table on
        easiedata
    """

    dfs = easie.get_easie_tables([easie_table_ref['artists_top_tracks']])
    artists_ids = dfs[
        easie_table_ref['artists_top_tracks']
    ]['artist_id'].unique()
    artists_ids = [
        a_id
        for artist_id in artists_ids
        for a_id in spotify.get_related_artists(artist_id)
    ]

    df = pd.DataFrame(spotify.get_artists_info(artists_ids))
    df = df[df['artist_followers_total'] <= core_settings['max_popularity']]
    top_tracks = []
    for artist_id in artists_ids:
        for market in core_settings['markets']:
            top_tracks += [
                {
                    'artist_id': artist_id,
                    'market': market,
                    **t
                }
                for t in spotify.get_artist_top_tracks_info(artist_id, market)
            ]

    df = pd.DataFrame(top_tracks).merge(df, how='left', on='artist_id')

    df_params = [{
        'table_name': easie_table_ref['related_artists_top_tracks'],
        'action': 'insert_with_df',
        'df': data_manipulation.sort_n_largest_market_popularity(
            artists_ids, df, core_settings
        ),
        'params': {'not_exists_create': True, 'replace': True}
    }]

    return easie, df_params


@easie_insertion
def track_recommendations(easie, spotify, core_settings, easie_table_ref):
    """
        Uses easie artists and related artists tracks data to get spotify
        recommendations

        Parameters
        ----------
        easie: Easie
            Easie instance
        spotify: Spotify
            Spotify instance
        core_settings: dict
            query_params: dict
                parameters to be passed on to
                spotify.get_recomendations_track_info
        easie_table_ref: dict
            key is the name of the core function and value the name of the table
            in easiedata
    """

    dfs = easie.get_easie_tables([
        easie_table_ref['artists_top_tracks'],
        easie_table_ref['related_artists_top_tracks']
    ])

    tracks_ids = list(
        dfs[easie_table_ref['artists_top_tracks']]['track_id'].unique()
    )
    tracks_ids += list(
        dfs[easie_table_ref['related_artists_top_tracks']]['track_id'].unique()
    )

    seed_tracks = [
        tracks_ids[random.randint(0, len(tracks_ids)-1)] for i in range(5)
    ]
    df_params = [{
        'table_name': easie_table_ref['track_recommendations'],
        'action': 'insert_with_df',
        'df': pd.DataFrame(spotify.get_recomendations_track_info({
            'seed_tracks': seed_tracks,
            **core_settings['query_params']
        })),
        'params': {'not_exists_create': True, 'replace': True}
    }]

    return easie, df_params
