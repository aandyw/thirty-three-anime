import csv
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle
from tqdm import tqdm


def cacheRelationship(userCsv, animeCsv, ratingCsv, chunkSize=100000):
    #Assume we do not modify userCsv and animeCsv

    #Create User Dictionary
    #Create Anime Dictionary

    #Write CSV (UserId, AnimeId, Rating)

    #Correlate UserName with UserId

    userDict = {}
    animeDict = {}

    userAnimeRelationship = {}
    animeUserRelationship = {}

    print("Creating userDict")
    cntr = 1
    dfs = pd.read_csv(userCsv, chunksize=chunkSize)
    for df in tqdm(dfs):
        df = df.dropna(subset=["username"])
        usernames = df["username"].values.tolist()
        for userName in usernames:
            if userName not in userDict:
                userDict[userName] = cntr
                cntr += 1

    with open("userDict.pckl", "wb") as f:
        pickle.dump(userDict, f)

    print("Creating animeDict")
    cntr = 1
    dfs = pd.read_csv(animeCsv, chunksize=chunkSize)
    for df in tqdm(dfs):
        df = df.dropna(subset=["anime_id"])
        animes = df["anime_id"].values.tolist()
        for animeId in animes:
            if animeId not in animeDict:
                animeDict[animeId] = cntr
                cntr += 1

    with open("animeDict.pckl", "wb") as f:
        pickle.dump(animeDict, f)

    print("Creating relationships")

    dfs = pd.read_csv(ratingCsv, chunksize=chunkSize)
    for df in tqdm(dfs):
        df = df.dropna(subset=["username","anime_id","my_score"])
        ratingValues = df[["username", "anime_id", "my_score"]].values.tolist()
        for userName, animeId, score in ratingValues:
            if (userName in userDict) and (animeId in animeDict):
                uid = userDict[userName]
                aid = animeDict[animeId]
                if uid not in userAnimeRelationship:
                    userAnimeRelationship[uid] = [[],[]]

                userAnimeRelationship[uid][0].append(aid)
                userAnimeRelationship[uid][1].append(score)

                if aid not in animeUserRelationship:
                    animeUserRelationship[aid] = [[],[]]

                animeUserRelationship[aid][0].append(uid)
                animeUserRelationship[aid][1].append(score)

    with open("userAnimeRelationship.pckl", "wb") as f:
        pickle.dump(userAnimeRelationship, f)

    with open("animeUserRelationship.pckl", "wb") as f:
        pickle.dump(animeUserRelationship, f)

    return userDict, animeDict, userAnimeRelationship, animeUserRelationship

def vectorTrain(SubMatrix, rating, lambdaReg):
    SubMatrix = np.transpose(SubMatrix)

    A = np.matmul(SubMatrix, np.transpose(SubMatrix)) + lambdaReg
    Ainv = np.linalg.inv(A)

    V = np.matmul(SubMatrix, np.transpose(rating))

    entVec = np.matmul(Ainv, V)
    # print(entVec[0].shape)
    return entVec

def ALStrain(iterations, userDict, animeDict, userAnimeRelationship, animeUserRelationship, dims=128, lambdaVal=0.065):
    numUsers = len(userDict)
    numAnime = len(animeDict)

    lambdaReg = np.identity(dims)*lambdaVal

    userMatrix = np.zeros((numUsers, dims))
    animeMatrix = np.random.uniform(low=-np.sqrt(3.0/np.sqrt(dims)), high=np.sqrt(3.0/np.sqrt(dims)), size=(numAnime, dims))

    users = sorted(list(userDict.values()))
    animes = sorted(list(animeDict.values()))

    for animeId in animes:
        if animeId in animeUserRelationship:
            animeMatrix[animeId-1,0] = np.mean(animeUserRelationship[animeId][1])

    for iteration in range(iterations):
        print(f"------Iteration {iteration}-------")
        print("Optimizing user matrix...")
        #User Optimization
        for i in tqdm(range(len(users))):
            user = users[i]
            if user in userAnimeRelationship:
                watchedAnime, rating = userAnimeRelationship[user]
                rating = np.array(rating,dtype=float)
                subMatrix = animeMatrix[np.array(watchedAnime)-1,:]

                userMatrix[i,:] = vectorTrain(subMatrix, rating, lambdaReg)
                # userVec = vectorTrain(subMatrix, rating, lambdaReg)

        #Anime Optimization

        print("Optimizing anime matrix...")
        for i in tqdm(range(len(animes))):
            anime = animes[i]
            if anime in animeUserRelationship:
                watchedUser, rating = animeUserRelationship[anime]
                rating = np.array(rating,dtype=float)
                subMatrix = userMatrix[np.array(watchedUser)-1,:]

                animeMatrix[i,:] = vectorTrain(subMatrix, rating, lambdaReg)

        print("Saving user matrix...")
        np.save("userMatrix.npy", userMatrix)
        print("Saving anime matrix...")
        np.save("animeMatrix.npy", animeMatrix)


# userDict, animeDict, userAnimeRelationship, animeUserRelationship = cacheRelationship("UserList.csv", "anime_cleaned.csv", "animelists_cleaned.csv")

userDict = pickle.load(open("userDict.pckl", "rb"))
animeDict = pickle.load(open("animeDict.pckl", "rb"))
userAnimeRelationship = pickle.load(open("userAnimeRelationship.pckl", "rb"))
animeUserRelationship = pickle.load(open("animeUserRelationship.pckl", "rb"))

animes = sorted(list(animeDict.values()))

avgRatings = []

for animeId in animes:
    if animeId in animeUserRelationship:
        avgRatings.append(np.mean(animeUserRelationship[animeId][1]))

referenceAnime = dict((v,k) for k,v in animeDict.items())

# ALStrain(20, userDict, animeDict, userAnimeRelationship, animeUserRelationship)

animeMatrix = np.load("animeMatrix.npy")

animeIds = [2049,5711,5469,4216,5285,4494,634,3010,3015,2539,4342,3803,3898,4386,759,5269,4400,489,3829,1014,4013]
ratings = [10,10,10,9,7,8,4,8,8,5,7,9,10,10,9,9,9,8,8,10,10]

subMatrix = animeMatrix[np.array(animeIds)-1,:]

lambdaReg = np.identity(128)*0.065

# print(subMatrix.shape)
userVector = vectorTrain(subMatrix, np.array(ratings), lambdaReg)
# print(userVector)
print(np.matmul(userVector, np.transpose(subMatrix)))

ratingInference = np.squeeze(np.matmul(np.expand_dims(userVector,0), np.transpose(animeMatrix)))


ratingAnimeId = [(i+1, ratingInference[i], avgRatings[i]) for i in range(ratingInference.size) if ratingInference[i] <= 10.1]

ratingAnimeId = sorted(ratingAnimeId, key=lambda x:0.8*x[1]+0.2*x[2], reverse=True)

print(ratingAnimeId)
animeIds = [referenceAnime[rating[0]] for rating in ratingAnimeId if rating[0] not in animeIds]


# print(animeIds)

# print(ratingAnimeId)
print(animeIds[:10])





