import os
import pandas as pd
import numpy as np

from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler

class AnimeData:

    def __init__(self, path_ratings, path_animes, path_features):
        self.animeID_to_title = {}
        self.title_to_animeID = {}

        user_df = pd.read_csv(path_ratings)
        anime_df = pd.read_csv(path_animes)
        features_df = pd.read_csv(path_features)

        self.animeID_to_title = anime_df.set_index('animeid')['title'].to_dict()
        self.title_to_animeID = {v: k for k, v in self.animeID_to_title.items()}

        # one hot encoding
        normalizer = MinMaxScaler()
        self.anime_features = normalizer.fit_transform(features_df)

        # creating anime and idx maps
        ratings_df = pd.DataFrame(user_df['animeid'].value_counts().reset_index().values, columns=['animeid', 'rated_by']).reset_index()
        ratings_df['index'] += 1
        rankings = ratings_df.set_index('animeid')['index'].to_dict()
        self.animeID_to_idx = defaultdict(int, rankings)
        self.idx_to_animeID = {v: k for k, v in self.animeID_to_idx.items()}
            
    def get_features(self):
        return self.anime_features

    def get_idx_from_id(self, animeID):
        return self.animeID_to_idx.get(animeID)

    def get_id_from_idx(self, idx):
        return self.idx_to_animeID.get(idx)

    def get_anime(self, animeID):
        if animeID in self.animeID_to_title:
            return self.animeID_to_title.get(animeID)
        else:
            return None
        
    def get_id(self, title):
        if title in self.title_to_animeID:
            return self.title_to_animeID.get(title)
        else:
            return None