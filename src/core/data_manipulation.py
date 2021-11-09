import pandas as pd

def sort_n_largest_market_popularity(artists_ids, df, core_settings):
    """
        Method to transform track dataframe according to top average market
        popularities
    """

    pop = df.pivot_table(
        index=['track_name', 'artist_id'],
        columns=['market'],
        values=['track_popularity'],
        aggfunc={'track_popularity': sum}
    )
    pop.columns = [
        '_'.join(multi_col) for multi_col in pop.columns
    ]
    pop.reset_index(inplace=True)

    avg_pop = sum([
        pop[f'track_popularity_{m}'] for m in core_settings['markets']
    ])/len(core_settings['markets'])

    pop.insert(len(pop.columns), 'track_popularity_avg', avg_pop)

    pop = pd.concat([
        pop[pop['artist_id']==artist_id].nlargest(
            core_settings['top_tracks'], 'track_popularity_avg'
        )
        for artist_id in artists_ids
    ])

    return pop.merge(
        df.drop(columns=['market']), how='left', on=['track_name', 'artist_id']
    ).sort_values('track_album_release_date').drop_duplicates(
        subset=['track_name', 'artist_id'], keep='first'
    )
