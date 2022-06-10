# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import os
import pickle

SEED = 42
model_file = './models.pickle'

def save_pickle(pickle_file, obj):
    with open(pickle_file, 'wb') as fp:
        pickle.dump(obj, fp)

def load_pickle(pickle_file):
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as fp:
            return pickle.load(fp)
    return None

def train():
    csv_train2 = './train_pre2_100.csv'
    csv_train2 = './train_pre2_10000.csv'
    csv_train2 = './train_pre2.csv'

    train_df = pd.read_csv(csv_train2)

    kinds = train_df['kind'].unique()

    print(kinds)
    models = {}

    for kind in kinds:
        print(kind)
        df = train_df.query(f'kind=="{kind}"')

        target = df['mode_price']

        dcols = ['Unnamed: 0', 'date', 'amount', 'area', 'ymd', 'mode_price', 'kind']
        df.drop(dcols, axis=1, inplace=True)

        X_train, X_test, y_train, y_test = train_test_split(
            df,
            target,
            test_size=0.1,
            shuffle=True,
            random_state=SEED
        )
        model = lgb.LGBMRegressor(
                n_estimators=1000,
                random_state = SEED,
        )

        model.fit(
            X_train, 
            y_train,
            eval_set=[(X_test, y_test), (X_train, y_train)]
            #verbose=-1 # 学習ログを省略
        )

        # 学習履歴の表示
        lgb.plot_metric(model)

        #print(model.predict(X_test))
        models[kind] = model

    save_pickle('models.pickle', models)

def predict():
    models = load_pickle(model_file)
    csv_test2 = './test_pre2.csv'

    csv_sub = './sample_submission.csv'

    test_df = pd.read_csv(csv_test2)
    sub_df = pd.read_csv(csv_sub)

    kinds = test_df['kind'].unique()

    #dcols = ['Unnamed: 0', 'date', 'amount', 'area', 'ymd', 'mode_price', 'kind']
    print(kinds)
    predicts = []

    for kind in kinds:
        print(kind)
        x = test_df.query(f'kind=="{kind}"')
        dcols = ['Unnamed: 0', 'date', 'area', 'ymd', 'kind']
        x.drop(dcols, axis=1, inplace=True)
        model = models[kind]
        predict = model.predict(x)
        print(predict)
        print(predict.shape)
        predicts.extend(predict)

    print(predicts)
    print(len(predicts))

    #kind,date,mode_price
    sub_df['mode_price'] = np.array(predicts)

    import datetime
    ymd_hms = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")

    sub_df.to_csv(f'sub_{ymd_hms}.csv', index=False)


if __name__ == '__main__':
    train()
    predict()
