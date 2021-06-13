import os
import pickle
import random

from sklearn.neighbors import NearestNeighbors
from algo.recsys.anime_data import AnimeData

SAVE_TO = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(os.path.dirname(__file__), SAVE_TO, 'knn_model.pickle')
SIMILARITIES_PATH = os.path.join(os.path.dirname(__file__), SAVE_TO, 'indices.pickle')
DISTANCES_PATH = os.path.join(os.path.dirname(__file__), SAVE_TO, 'distances.pickle')

PATH_RATINGS = os.path.join(os.path.dirname(__file__), 'data', 'ratings.csv')
PATH_ANIMES = os.path.join(os.path.dirname(__file__), 'data', 'animes.csv')
PATH_FEATURES = os.path.join(os.path.dirname(__file__), 'data', 'anime_features.csv')

class KNN:

    def __init__(self):

        print("Compiling anime dataset...")
        self.data = AnimeData(PATH_RATINGS, PATH_ANIMES, PATH_FEATURES)

        anime_features = self.data.get_features()

        print("Building KNN model...")
        if os.path.isfile(MODEL_PATH) and os.path.isfile(SIMILARITIES_PATH) and os.path.isfile(DISTANCES_PATH):
            print("Loading model and item similarities...")
            self.model = pickle.load(open(MODEL_PATH, "rb"))
            self.indices = pickle.load(open(SIMILARITIES_PATH, "rb"))
            self.distances = pickle.load(open(DISTANCES_PATH, "rb"))
        else:
            self.model = NearestNeighbors(n_neighbors=11, algorithm='ball_tree')
            self.model.fit(anime_features)

            print("Creating item similarities...")
            self.distances, self.indices = self.model.kneighbors(anime_features)

            if not os.path.exists(SAVE_TO):
                os.makedirs(SAVE_TO)
                
            with open(MODEL_PATH, "wb") as f:
                pickle.dump(self.model, f)
            
            with open(SIMILARITIES_PATH, "wb") as f:
                pickle.dump(self.indices, f)
            
            with open(DISTANCES_PATH, "wb") as f:
                pickle.dump(self.distances, f)

    def get_top_n(self, animeIDs, n=10):

        # lst = []
        # recommendations = []

        # for animeID in animeIDs:
        #     if self.data.get_anime(animeID) is not None:
        #         print("Getting recommendations for {}".format(animeID))
        #         idx = self.data.get_idx_from_id(animeID)

        #         for i, dist in zip(self.indices[idx], self.distances[idx]):
        #             predicted = self.data.get_id_from_idx(i)
        #             # predicted = self.data.get_anime(id)
        #             if (predicted is not None) and \
        #                 (int(animeID) != int(predicted)) and \
        #                 (predicted not in lst):
        #                 lst.append((predicted, dist))
        #     else:
        #         print("{} does not exist in database".format(animeID))

        # lst = sorted(lst, key=lambda x: x[1])
        # for i in range(n):
        #     print(lst[i][0])
        #     recommendations.append(lst[i][0]) # get only anime id

        # return recommendations[:n]

        recommendations = []

        for animeID in animeIDs:
            if self.data.get_anime(animeID) is not None:
                print("Getting recommendations for {}".format(animeID))
                idx = self.data.get_idx_from_id(animeID)

                for i, dist in zip(self.indices[idx], self.distances[idx]):
                    predicted = self.data.get_id_from_idx(i)
                    # predicted = self.data.get_anime(id)
                    if (predicted is not None) and \
                        (int(animeID) != int(predicted)) and \
                        (predicted not in recommendations):
                        recommendations.append(predicted)
            else:
                print("{} does not exist in database".format(animeID))

        random.shuffle(recommendations)
        return recommendations[:n]
