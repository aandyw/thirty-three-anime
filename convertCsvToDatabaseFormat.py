import csv
import pandas as pd
import numpy as np
from tqdm import tqdm


def convertCsvToDatabaseFormat(userCsv, animeCsv, ratingCsv, chunkSize=100000):
    #Assume we do not modify userCsv and animeCsv

    #Create User Dictionary
    #Create Anime Dictionary

    #Write CSV (UserId, AnimeId, Rating)

    #Correlate UserName with UserId

    userDict = {}
    animeDict = {}

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

    print("Creating curatedRatings.csv")
    with open("curatedRatings.csv","w") as f:
        ratingWriter = csv.writer(f)
        ratingWriter.writerow(["userId","animeId","rating"])

        dfs = pd.read_csv(ratingCsv, chunksize=chunkSize)
        for df in tqdm(dfs):
            ratingValues = df[["username", "anime_id", "my_score"]].values.tolist()
            for userName, animeId, score in ratingValues:
                if (userName in userDict) and (animeId in animeDict):
                    ratingWriter.writerow([userDict[userName], animeDict[animeId], score])

convertCsvToDatabaseFormat("UserList.csv", "anime_cleaned.csv", "animelists_cleaned.csv")
