import numpy as np
import pandas as pd
import requests
import time
import argparse
from tqdm import tqdm

# arg parser for continuous scraping
my_parser = argparse.ArgumentParser(description='')
my_parser.add_argument('--cont', default=True,
                       action='store_false', help='to continue with last CSV')
my_parser.add_argument('-s', '--start', type=int, required=True)
args = my_parser.parse_args()

SAVE_PATH = 'data/AnimeImages.csv'
# ENDPOINT = 'http://localhost:2375/v3/anime/{anime_id}/pictures'
ENDPOINT = 'https://api.jikan.moe/v3/anime/{anime_id}/pictures'

if args.cont:
    print("Starting new CSV...")
    malDataPath = 'data/myanimelist/AnimeList.csv'
    df = pd.read_csv(malDataPath)
    cols = ['anime_id', 'title', 'type', 'producer', 'studio', 'genre']
    data = pd.DataFrame(df, columns=cols)
    # create new images column
    data['images'] = ''
else:
    print("Continuing from last CSV...")
    malDataPath = 'data/AnimeImages.csv'
    cols = ['id', 'anime_id', 'title', 'type',
            'producer', 'studio', 'genre', 'images']
    df = pd.read_csv(malDataPath)
    data = pd.DataFrame(df, columns=cols)

start = args.start
end = len(data.index)

print("Scraping from rows {start} to {end}".format(start=start, end=end-1))

# image scraping loop
for i in tqdm(range(start, end)):
    response = requests.get(ENDPOINT.format(anime_id=data.iloc[i]['anime_id']))
    imgs = set()

    for attempt in range(3):
        try:
            for img in response.json()['pictures']:
                imgs.add(img['large'])
            data.at[i, 'images'] = imgs
            # time.sleep(2)  # MAL request delay
            if(i % 2 == 0):
                time.sleep(3)  # Jikan API delay
        except:
            print(response.json())
        else:
            break
    else:
        data.at[i, 'images'] = 'N/A'

    if (i % 20 == 0):
        data.to_csv(SAVE_PATH, index=False)

data.to_csv(SAVE_PATH, index=False)
