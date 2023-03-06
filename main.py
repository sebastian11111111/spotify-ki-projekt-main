import time
from copy import copy

import numpy as np
from scipy import stats
import statsmodels.api as sm
import pandas as pd
from sklearn import linear_model

from spotify import Spotify


def load_track_data():
    track_data = pd.read_csv("data/track_data.csv")
    track_data = track_data[[
        'track_id'
        , 'artists'
        , 'track_name'
        , 'popularity'
        , 'duration_ms'
        , 'explicit'
        , 'danceability'
        , 'energy'
        , 'key'
        , 'loudness'
        , 'mode'
        , 'speechiness'
        , 'acousticness'
        , 'instrumentalness'
        , 'liveness'
        , 'valence'
        , 'tempo'
        , 'time_signature'
        , 'track_genre']]
    print(track_data)
    track_data["artists"] = track_data["artists"].str.split(";")
    output = track_data.explode("artists")

    output.to_csv('output/track_data_splited_artists.csv')
    print(output)





def init_bullshit():
    base = pd.read_csv("data/track_popularity.csv")
    base = base[['artists', 'track_name', 'totalstreams']]
    filler = pd.read_csv('data/track_information.csv')
    filler = filler[
        ['artists', 'track_name', 'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode',
         'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']]

    filler['explicit'] = filler['explicit'].map(lambda x: 1 if x == 'True' else 0)
    base['artists'] = base['artists'].map(lambda x: str(x).upper())
    base['track_name'] = base['track_name'].map(lambda x: str(x).upper())
    filler['artists'] = filler['artists'].map(lambda x: str(x).upper())
    filler['track_name'] = filler['track_name'].map(lambda x: str(x).upper())
    output1 = base.merge(filler, on=['artists', 'track_name'], how="inner")
    unique_out1 = output1[['artists', 'track_name']].value_counts().reset_index(name='count')
    filler['artists'] = filler['artists'].map(lambda x: x.split(';')[0])
    output2 = base.merge(filler, on=['artists', 'track_name'], how="inner")
    unique_out2 = output2[['artists', 'track_name']].value_counts().reset_index(name='count')
    print(unique_out1)
    print(unique_out2)


def load_spotify():
    spotify = Spotify()
    base = pd.read_csv("data/track_popularity.csv")
    output = []

    artists = base['artists']

    artists = set(artists)

    for artist in artists:
        try:
            element = spotify.get_artist(artist)
            output.append((element['name'], element['popularity'], element['followers']['total']))
            print(f"{element['name']} was added")
        except:
            time.sleep(10)

    pd.DataFrame(output, columns=['artists', 'popularity', 'follower']).to_csv('output/artists_output.csv')


def linear_regression():
    base = pd.read_csv("output/output2.csv")
    for column in list(base.keys())[3:]:
        base[column] = base[column].astype(float)

    X = base[list(base.keys())[4:]]
    y = base['totalstreams']

    mod = sm.OLS(y, X)
    fii = mod.fit()
    p_values = fii.summary2().tables[1]['P>|t|']
    my_dictionary = {k: round(v, 3) for k, v in dict(p_values).items()}

    print(my_dictionary)
    print(fii.summary2())

    row = list(base.iloc[1])[4:]
    print(row)

    # pred = fii.forecast(row)
    # print(pred)

    # Predict at x=2.5
    # X_test = row  # "1" refers to the intercept term
    # result = fii.get_prediction(X_test)  # alpha = significance level for confidence interval
    # result.summary_frame(alpha=0.05)


def add_artists():
    base = pd.read_csv('output/output.csv')
    filler = pd.read_csv('output/artists_output.csv')
    filler['artists'] = filler['artists'].map(lambda x: str(x).upper())

    output = base.merge(filler[['artists', 'popularity', 'follower']], on='artists', how="inner")

    output = output[list(output.keys())[1:]]

    output.to_csv('output/output2.csv')


if __name__ == '__main__':
    # linear_regression()
    # init_bullshit()
    load_track_data()
    # TODO: output2 > output -> Problem :(
    # TODO: Hohe Verlustquote 10000 -> 4000
    # TODO: Neuronale Netze
