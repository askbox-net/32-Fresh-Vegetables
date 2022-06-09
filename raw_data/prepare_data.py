# -*- coding:utf-8 -*-

import pandas as pd


if __name__ == '__main__':
    csv_weather = './weather100.csv'
    weather_df = pd.read_csv(csv_weather)

    weather_df['ymd'] = pd.to_datetime(weather_df['date'], format="%Y%m%d")
    weather_df.set_index('ymd', inplace=True)

    print(weather_df.resample('W').mean())

    #print(weather_df)
    #print(weather_df.info())
