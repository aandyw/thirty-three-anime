
import os
import requests
from recsys.algo.als import ALS

SEARCH_ENDPOINT = 'https://api.jikan.moe/v3/search/anime'
ANIME_ENDPOINT = 'https://api.jikan.moe/v3/anime/{id}'

recommender = ALS(
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\UserList.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\anime_cleaned.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\animelists_cleaned.csv"
    )


def get_search(title):
    try:
        params = {'q': title, 'type': 'anime'}
        r = requests.get(SEARCH_ENDPOINT, params=params)
        results = r.json()['results']  # LIST OF RESULTS
        # print(results)
        return results
    except:
        return []

def perform_inference(animeids):
    results = recommender.inference(animeids, [10]*9)
    return results[:10]

def get_animes(animeids):
    try:
        results = []
        for animeid in animeids:
            r = requests.get(ANIME_ENDPOINT.format(id=animeid))
            data = r.json()
            results.append({
                'title': data['title'], 
                'url' : data['url'], 
                'image_url' :data['image_url']
            })
        
        return results
    except:
        return None