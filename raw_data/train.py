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


def get_vec(x):
    area = x['area']
    ymd = x['ymd']
    areas = area.split('_')
    tmps = []
    m = {'アメリカ': '全国',
        'カナダ': '全国',
        'トンガ': '全国',
        'ニュージーランド': '全国',
        'メキシコ': '全国',
        '中国': '全国',
        '佐賀': '佐賀',
        '兵庫': '神戸',
        '北海道': '帯広',
        '千葉': '千葉',
        '各地': '全国',
        '和歌山': '和歌山',
        '国内': '全国',
        '埼玉': '熊谷',
        '宮城': '仙台',
        '宮崎': '宮崎',
        '山形': '山形',
        '山梨': '甲府',
        '岩手': '盛岡',
        '徳島': '徳島',
        '愛媛': '松山',
        '愛知': '名古屋',
        '新潟': '新潟',
        '東京': '東京',
        '栃木': '宇都宮',
        '沖縄': '那覇',
        '熊本': '熊本',
        '神奈川': '横浜',
        '福岡': '福岡',
        '福島': '福島',
        '秋田': '秋田',
        '群馬': '前橋',
        '茨城': '水戸',
        '長崎': '長崎',
        '長野': '長野',
        '青森': '青森',
        '静岡': '浜松',
        '香川': '高松',
        '高知': '高知',
        '鹿児島': '鹿児島'}

    for area in areas:
        #print('area: ', area)
        if area in m.keys():
            area = m[area]
        tmps.append(weathers_weekly[area].query(f'ymd <= "{ymd}"').head(5).values.reshape(-1))
    vs = np.mean(tmps, axis=0).tolist()
    for k, v in zip([f"v_{i}" for i in range(len(vs))], vs):
        x[k] = v

    #return weathers_weekly[area].query(f'ymd <= "{ymd}"').head(5).values.reshape(-1)
    #print('len: ', len(tmps))
    #return pd.DataFrame(np.mean(tmps, axis=0))
    #return pd.DataFrame(np.mean(tmps, axis=0))
    return x


if __name__ == '__main__':
    pickle_weather_weekly = 'weathers_weekly.pickle'
    csv_weather = './weather.csv'
    csv_train = './train.csv'
    csv_test = './test.csv'
    weathers_weekly = load_pickle(pickle_weather_weekly)
    """
    print(get_vec('千葉_東京', '2019-01-01'))
    print(get_vec('千葉', '2019-01-01'))
    print(get_vec('東京', '2019-01-01'))

    print(get_vec('千葉_仙台', '2019-01-01'))
    print(get_vec('千葉', '2019-01-01'))
    print(get_vec('仙台', '2019-01-01'))
    """

    test_df = pd.read_csv(csv_test)
    test_df['ymd'] = pd.to_datetime(test_df['date'], format='%Y%m%d')

    print(test_df)
    df = test_df.apply(lambda x: get_vec(x), axis=1)

    #print(df.values)
    #print(df.values.shape)

    print(df)
    print(df.shape)

    df.to_csv('test_pre2.csv')
    exit(0)

    train_df = pd.read_csv(csv_train)
    train_df['ymd'] = pd.to_datetime(train_df['date'], format='%Y%m%d')

    print(train_df)

    #df = train_df.query('area=="千葉"').apply(lambda x: get_vec(x), axis=1)
    df = train_df.apply(lambda x: get_vec(x), axis=1)

    #print(df.values)
    #print(df.values.shape)

    print(df)
    print(df.shape)

    df.to_csv('train_pre2.csv')

    #print(weathers_weekly)
"""
    for k, weathers in weathers_weekly.items():
        print(k, weathers.shape)

"""
