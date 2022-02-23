# Get the meta data features of each track in the charts
# reference https://stmorse.github.io/journal/spotify-api.html
# https://towardsdatascience.com/discovering-spotify-wrapped-an-extended-data-exploration-1975a8b7af29

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import client_id, client_secret
import pandas as pd
from time import sleep

# Import credentials from credentials file. Credentials are set up at developer.spotify.com
CLIENT_ID = client_id
CLIENT_SECRET = client_secret

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def retrieve_track_data(search_track_ids):
    """Function to retrieve the playlist"""

    song_meta = dict(id=[], acousticness=[], danceability=[], energy=[], instrumentalness=[], key=[],
                     liveness=[], loudness=[], speechiness=[], tempo=[], time_signature=[], valence=[])

    meta = sp.audio_features(search_track_ids)
    current_chart = pd.DataFrame()
    #print (meta[0])

    for song in meta:
        # song id
        song_meta['id'].append(song['id'])
        song_meta['acousticness'].append(song['acousticness'])
        #song_meta['popularity'].append(song['popularity'])
        song_meta['danceability'].append(song['danceability'])
        song_meta['energy'].append(song['energy'])
        song_meta['instrumentalness'].append(song['instrumentalness'])
        song_meta['key'].append(song['key'])
        song_meta['liveness'].append(song['liveness'])
        song_meta['loudness'].append(song['loudness'])
        song_meta['speechiness'].append(song['speechiness'])
        song_meta['tempo'].append(song['tempo'])
        song_meta['time_signature'].append(song['time_signature'])
        song_meta['valence'].append(song['valence'])

        song_meta_df = pd.DataFrame.from_dict(song_meta)
        current_chart = current_chart.append(song_meta_df, ignore_index=True)
        #print (current_chart.head())

    # final_df.to_csv("playlisttest.csv")
    return current_chart


# Run this once to split out the spotify_ids

# hits_df = pd.read_excel('spotify_sa_chart.xlsx', engine="openpyxl")
# song_ids=[]
# for url in hits_df['spotify_url'].to_list():
#     song_id = url.split('/')[-1]
#     song_ids.append(song_id)
# hits_df['song_ids']=song_ids
# hits_df.to_excel('spotify_sa_chart.xlsx', engine="openpyxl")

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


chart_features_df = pd.DataFrame()
hits_df = pd.read_excel('spotify_sa_chart.xlsx', engine="openpyxl")

song_ids = hits_df['song_ids'].to_list()
song_ids = list(dict.fromkeys(song_ids))

chunked_list = chunks(song_ids, 100)
for chunk in chunked_list:
    data = retrieve_track_data(chunk)
    
    chart_features_df= chart_features_df.append(data, ignore_index=True)
    sleep(30)
chart_features_df.to_excel("chart_features.xlsx", engine="openpyxl")
# for track_id in song_ids:
