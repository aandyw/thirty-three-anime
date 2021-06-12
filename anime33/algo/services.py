import os
import requests
from algo.recsys.knn import KNN

ANIME_ENDPOINT = 'https://api.jikan.moe/v3/anime/{id}'

recommender = KNN()


def perform_inference(animeids):
    results = recommender.get_top_n(animeids)
    return results

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