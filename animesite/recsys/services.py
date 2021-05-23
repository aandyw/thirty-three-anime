
import os
import requests
from recsys.algo.als import ALS

SEARCH_ENDPOINT = 'https://api.jikan.moe/v3/search/anime'


def get_search(title):
    try:
        params = {'q': title, 'type': 'anime'}
        r = requests.get(SEARCH_ENDPOINT, params=params)
        results = r.json()['results']  # LIST OF RESULTS
        return results
    except:
        return []

def perform_inference(animeids):
    recommender = ALS(
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\UserList.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\anime_cleaned.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\animelists_cleaned.csv"
    )
    
    results = recommender.inference(animeids, [10]*9)
    return results[:10]