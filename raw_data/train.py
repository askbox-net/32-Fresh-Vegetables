# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import os
import pickle

def load_pickle(pickle_file):
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as fp:
            return pickle.load(fp)
    return None


def get_vec(area, ymd):
    return weathers_weekly[area].query(f'ymd <= "{ymd}"').head(5).T


if __name__ == '__main__':
    pickle_weather_weekly = 'weathers_weekly.pickle'
    csv_weather = './weather.csv'
    csv_train = './train.csv'
    csv_test = './test.csv'

    train_df = pd.read_csv(csv_train)
    train_df['ymd'] = pd.to_datetime(train_df['date'], format='%Y%m%d')

    weathers_weekly = load_pickle(pickle_weather_weekly)
    print(train_df)

    df = train_df.query('area=="千葉"').apply(lambda x: get_vec(x['area'], x['ymd']), axis=1)

    print(df)


    #print(weathers_weekly)
"""
    for k, weathers in weathers_weekly.items():
        print(k, weathers.shape)

"""
