import os
import requests
from algo.recsys.als import ALS

ANIME_ENDPOINT = 'https://api.jikan.moe/v3/anime/{id}'

recommender = ALS(
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\UserList.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\anime_cleaned.csv", 
     "D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\animelists_cleaned.csv"
    )


def perform_inference(animeids):
    results = recommender.inference(animeids)
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