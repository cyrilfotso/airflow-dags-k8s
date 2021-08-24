import re
import os
import time
import random
import pandas as pd
from pathlib import Path


PARENT_PATH = str(Path(__file__).resolve().parents[1])


def set_pattern(x):
    pattern = r'[(A-Z)]\w+,([A-Z])\w+'
    res = re.match(pattern, x)
    if res:
        x = x.replace(',', ', ')
    return x


def data_processing():
    sleep_times = [1, 4, 5, 10]
    print('sleep_times', sleep_times)
    df = pd.read_csv(os.path.join(PARENT_PATH, 'data', 'tweets.csv'))
    print(df.head(10))
    time.sleep(random.choice(sleep_times))
    df.dropna(inplace=True)
    print(df.dtypes)
    df['Tweet Location'] = df['Tweet Location'].astype('string')
    df['Tweet Content'] = df['Tweet Content'].str.lower()
    df['Tweet Location'].unique()
    df['Tweet Location'] = df['Tweet Location'].apply(lambda x: set_pattern(x))
    time.sleep(random.choice(sleep_times))
    print(df.head(20))
    return df


if __name__ == '__main__':
    data_processing()

