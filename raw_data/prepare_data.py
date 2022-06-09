# -*- coding:utf-8 -*-

import pandas as pd
import pickle
import os


def load_pickle(pickle_file):
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as fp:
            return pickle.load(fp)
    return None

def save_pickle(pickle_file, obj):
    with open(pickle_file, 'wb') as fp:
        pickle.dump(obj, fp)

if __name__ == '__main__':

    weather_pickle = 'weathers.pickle'
    weather_weekly_pickle = 'weathers_weekly.pickle'
    csv_weather = './weather100.csv'
    csv_weather = './weather.csv'

    weathers = load_pickle(weather_pickle)

    if weathers is None:
        weather_df = pd.read_csv(csv_weather)
        print(weather_df)
        areas = weather_df['area'].unique()
        print(areas)
        print(len(areas))
        weathers = {}

        for area in areas:
            weathers[area] = weather_df.query(f"area=='{area}'")

        print(weathers)
        save_pickle(weather_pickle, weathers)

    print(weathers)
    weathers_weekly = {}

    for k, weather_df in weathers.items():
        weather_df['ymd'] = pd.to_datetime(weather_df['date'], format="%Y%m%d")
        weather_df.drop(columns=['area', 'date', 'max_temp_time', 'min_temp_time'], axis=1, inplace=True)
        weather_df.set_index('ymd', inplace=True)
        print(k)
        print(weather_df)
        weathers_weekly[k] = weather_df.resample('W').mean()
        #break

    weather_df = pd.read_csv(csv_weather)
    weather_df['ymd'] = pd.to_datetime(weather_df['date'], format="%Y%m%d")
    weather_df.drop(columns=['area', 'date', 'max_temp_time', 'min_temp_time'], axis=1, inplace=True)
    weathers_weekly['全国'] = weather_df.groupby('ymd').mean().resample('W').mean()
    #print(weathers_weekly)
    save_pickle(weather_weekly_pickle, weathers_weekly)

    exit(0)

    weather_df['ymd'] = pd.to_datetime(weather_df['date'], format="%Y%m%d")
    weather_df.set_index('ymd', inplace=True)

    print(weather_df.resample('W').mean())

    #print(weather_df.info())
