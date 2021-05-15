import numpy as np
import csv
import pickle
from tqdm import tqdm
from alsDatabaseManager import UserAnimeDatabase

#Anime User/Movie Init
#Save into pickle

#Linear algorithm --> O(n)

#ALS training

class ALS:
    def __init__(self, dims=128, lambdaConst=0.065):
        self.dims = dims

        self.lambdaReg = np.expand_dims(np.identity(dims)*lambdaConst, 0)

        self.database = UserAnimeDatabase(dims=dims)

        self.userList = self.database.getUserList()
        self.animeList = self.database.getAnimeList()

    def initializeAnimeCache(self):
        self.database.onlyInitializeALS()

    def vectorTrain(self, trainTarget, batchSize=512):
        #User if trainTarget = 0, Anime if trainTarget = 1

        SubMatrixBatch = []
        ratingBatch = []
        entIds = []

        maxCols = 0

        if trainTarget == 0:
            lst = self.userList
        else:
            lst = self.animeList

        for ent in tqdm(lst):
            if trainTarget == 0:
                SubMatrix, rating = self.database.getUserALSFeatures(ent[0])
            else:
                SubMatrix, rating = self.database.getAnimeALSFeatures(ent[0])

            if SubMatrix is not None:
                SubMatrix = np.transpose(SubMatrix)

                entIds.append(ent[0])
                SubMatrixBatch.append(SubMatrix)
                ratingBatch.append(np.expand_dims(rating,0))

                if maxCols < rating.size:
                    maxCols = rating.size

            if len(ratingBatch) >= batchSize:
                SubMatrixBatch = [np.pad(SubMatrix, ((0,0),(0,maxCols-SubMatrix.shape[1])), constant_values=0) for SubMatrix in SubMatrixBatch]
                ratingBatch = [np.pad(rating, ((0,0),(0,maxCols-rating.size)), constant_values=0) for rating in ratingBatch]

                SubMatrixBatch = np.stack(SubMatrixBatch)
                ratingBatch = np.stack(ratingBatch)

                A = np.matmul(SubMatrixBatch, np.transpose(SubMatrixBatch, (0,2,1))) + self.lambdaReg
                Ainv = np.linalg.inv(A)

                V = np.matmul(SubMatrixBatch, np.transpose(ratingBatch,(0,2,1)))

                entVec = np.squeeze(np.matmul(Ainv, V))
                # print(entVec.shape)
                # print(entVec[0].shape)

                if trainTarget == 0:
                    [self.database.storeUserFeature(entIds[i], entVec[i]) for i in range(len(entIds))]
                else:
                    [self.database.storeAnimeFeature(entIds[i], entVec[i]) for i in range(len(entIds))]

                SubMatrixBatch = []
                ratingBatch = []
                entIds = []
                maxCols = 0


    def ALSTrain(self, iterations):
        #Train Users

        for iteration in range(iterations):
            print(f"-----Iteration {iteration}-----")
            print("Training User Vectors")
            self.vectorTrain(0)
            print("Training Anime Vectors")
            self.vectorTrain(1)


            #for animeId in animeRatingCache.keys():
            #    pass
            #    ratingVector = pickle.load(open("{}/{}.pckl".format(self.animeRatingCacheDir, animeId), "rb"))
            #    #Get user submatrix
            #    #animeId
            #    #rating row vector

        #Train Anime

#Dummy code

als = ALS()
als.ALSTrain(1)
# als.userVectorTrain()
# try:
#     als.userVectorTrain()
#     als.database.disconnect()
# except:
#     als.database.disconnect()

# als.initialize()
# als.ALSTrain(1)



