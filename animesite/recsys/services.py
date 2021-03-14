
import os
import requests

SEARCH_ENDPOINT = 'https://api.jikan.moe/v3/search/anime'


def get_search(title):
    try:
        params = {'q': title, 'type': 'anime'}
        r = requests.get(SEARCH_ENDPOINT, params=params)
        results = r.json()['results']  # LIST OF RESULTS
        return results
    except:
        return []
