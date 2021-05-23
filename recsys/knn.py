import pandas as pd
import numpy as np
import os
import gc
import pickle

from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from fuzzywuzzy import fuzz

SAVE_TO = 'models'
MODEL_PATH = os.path.join(os.getcwd(), SAVE_TO, 'knn.sav')
SPARSE_PATH = os.path.join(os.getcwd(), SAVE_TO, 'sparse.npz')
MAP_PATH = os.path.join(os.getcwd(), SAVE_TO, 'map.pickle')


class KnnRecommender:

    def __init__(self, path_animes, path_users):

        if os.path.isfile(MODEL_PATH) and os.path.isfile(SPARSE_PATH):
            self.model = pickle.load(open(MODEL_PATH, "rb"))
            self.anime_user_sparse = sparse.load_npz(SPARSE_PATH)
            self.anime_map = pickle.load(open(MAP_PATH, "rb"))
        else:
            anime_map, user_df = self.__prep(path_animes, path_users)
            self.anime_map = anime_map

            self.model = NearestNeighbors()
            self.anime_user_sparse = self.__sparse(user_df)
            self.model.fit(self.anime_user_sparse)

            if not os.path.exists(SAVE_TO):
                os.makedirs(SAVE_TO)
                
            pickle.dump(self.model, open(MODEL_PATH, "wb"))
            sparse.save_npz(SPARSE_PATH, self.anime_user_sparse)
            pickle.dump(self.anime_map, open(MAP_PATH, "wb"))

        self.reverse_anime_map = {v: k for k, v in self.anime_map.items()}
    
    def __prep(self, path_animes, path_users):
        user_df = pd.read_csv(path_users)
        # increase ratings by 1
        # unseen anime will have 0 and ratings go from 1-11
        user_df['my_score'] += 1

        # Z-score normalization
        arr = np.asarray(list(user_df['my_score']))
        mean = np.mean(arr)
        std = np.std(arr)

        user_df['my_score'] -= mean
        user_df['my_score'] /= std

        # splicing
        user_df = user_df.iloc[:25379534, :]
        anime_df = pd.read_csv(path_animes, usecols=['anime_id', 'title'])

        # creating maps from index to anime & anime_id
        anime_ids = list(anime_df['anime_id'])
        anime_titles = list(anime_df['title'])
        id_title_map = {
            anime_ids[i]:anime_titles[i] for i in range(len(anime_ids))
        }

        anime_map = {}
        for i, anime_id in enumerate(list(user_df['anime_id'].unique())):
            anime_title = id_title_map.get(anime_id)
            anime_map[anime_title] = i

        return anime_map, user_df

    def __sparse(self, user_df):
        print("Number of unique users: ", len(user_df['uid'].unique()))
        print("Number of anime rated by users: ", len(user_df['anime_id'].unique()))

        anime_user_mat = user_df.pivot(
            index='anime_id',
            columns='uid',
            values='my_score'
        ).fillna(0)

        anime_user_sparse = csr_matrix(anime_user_mat.values)

        print("Sparse matrix created")

        # clean up RAM
        del anime_user_mat, user_df
        gc.collect()

        return anime_user_sparse

    def __fuzzy_matching(self, fav_anime, min_ratio=60):
        """
        Finds the closest matching title from the user-anime matrix given fav_anime
        """

        matched = None
        ratio = min_ratio
        for title, idx in self.anime_map.items():
            match_ratio = fuzz.ratio(title.lower(), fav_anime.lower())
            if match_ratio >= ratio:
                ratio = match_ratio # set new greater ratio
                matched = (title, idx)
        
        return matched[1] # return the idx

    def inference(self, fav_anime, k=10):
        """
        Recommends closest k anime matches
        """
        print("Recommendations for {}:".format(fav_anime))

        idx = self.__fuzzy_matching(fav_anime)
        # print(len(list(self.anime_map)))

        distances, indices = self.model.kneighbors(
            self.anime_user_sparse[idx], n_neighbors=k+1
        )

        raw_recommends = (
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                )
            )
        )

        for (idx, dist) in raw_recommends:
            print(self.reverse_anime_map[idx], dist)


if __name__ == '__main__':
    recommender = KnnRecommender(
        os.path.join('D:\\Development\\Projects\\thirty-three-anime\\data\\myanimelist\\AnimeList.csv'),
        os.path.join('D:\\Development\\Projects\\thirty-three-anime\\data\\users_cleaned.csv')
    )
    recommender.inference('Ookami to Koushinryou')
    # recommender.inference('Shingeki no Kyojin')