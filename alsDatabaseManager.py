import mysql.connector
import pandas as pd
from tqdm import tqdm
import numpy as np
import pickle
import os

def createUserAnimeDatabase():
    mydb = mysql.connector.connect(
      host="localhost",
      user="userName",
      password="Passw*rd"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE userAnimeRating")

class UserAnimeDatabase:
    def __init__(self, userVectorDir='userVectors', animeVectorDir='animeVectors', dims=128):
        self.mydb = mysql.connector.connect(
          host="localhost",
          user="brian",
          password="Kyh02031!",
            database="userAnimeRating"
        )
        self.mycursor = self.mydb.cursor()
        self.dims = dims
        self.userVectorDir = userVectorDir
        self.animeVectorDir = animeVectorDir

    def completeInitialize(self, userCsvDir, animeCsvDir, ratingCsvDir):
        #Initialize database with pre-recorded CSV data

        #Assume there are no tables created yet
        #Format database tables just in case

        print("Formatting User Vector Cache")
        self.formatUserVectorCache()
        print("Formatting Anime Vector Cache")
        self.formatAnimeVectorCache()

        print("Dropping Users")

        self.dropTable("users")
        print("Dropping Anime")
        self.dropTable("animes")
        print("Dropping Ratings")
        self.dropTable("ratings")

        self.createUserTable()
        self.createAnimeTable()
        self.createRatingsTable()

        print("Initializing Users")
        self.initUsers(userCsvDir)
        print("Initializing Anime")
        self.initAnime(animeCsvDir)
        print("Initializing Ratings")
        self.initRating(ratingCsvDir)

        print("Caching User Vector")
        self.cacheUserVector()
        print("Caching Anime Vector")
        self.cacheAnimeVector()

    def onlyInitializeALS(self):
        print("Formatting Anime Vector Cache")
        self.formatAnimeVectorCache()
        print("Caching Anime Vector")
        self.cacheAnimeVector()

    def createRatingsTable(self):
        self.mycursor.execute("CREATE TABLE ratings (rid INT AUTO_INCREMENT PRIMARY KEY, userId INT, animeId INT, rating INT, KEY idx_userId (userId), KEY idx_animeId (animeId))")
        self.mydb.commit()

    def createUserTable(self):
        self.mycursor.execute("CREATE TABLE users (uid INT AUTO_INCREMENT PRIMARY KEY, userName VARCHAR(255), gender VARCHAR(255), UNIQUE KEY idx_userName (userName) USING BTREE)")
        self.mydb.commit()

    def createAnimeTable(self):
        #animeId is redundant, but since this is a prototype, we just use Id that myanimelist provided us
        #Will remove animeId in the near future
        self.mycursor.execute("CREATE TABLE animes (aid INT AUTO_INCREMENT PRIMARY KEY, animeId INT, animeTitle VARCHAR(255), animeTitleEnglish VARCHAR(255), UNIQUE KEY idx_animeId (animeId) USING BTREE)")

    def initUsers(self, userCsvDir, chunkSize=100000):
        dfs = pd.read_csv(userCsvDir, chunksize=chunkSize)
        sql = "INSERT INTO users (userName, gender) VALUES (%s, %s)"
        for df in tqdm(dfs):
            df = df.dropna(subset=["username"])
            df = df.fillna(0)
            userInfo = df[["username","gender"]].values.tolist()

            self.mycursor.executemany(sql, df[["username","gender"]].values.tolist())
            self.mydb.commit()

    def initAnime(self, animeCsvDir, chunkSize=100000):
        dfs = pd.read_csv(animeCsvDir, chunksize=chunkSize)
        sql = "INSERT INTO animes (animeId, animeTitle, animeTitleEnglish) VALUES (%s, %s, %s)"
        for df in tqdm(dfs):
            df = df.dropna(subset=["anime_id"])
            df = df.fillna(0)

            self.mycursor.executemany(sql, df[["anime_id","title","title_english"]].values.tolist())
            self.mydb.commit()

    def initRating(self, ratingCsvDir, chunkSize=100000):
        dfs = pd.read_csv(ratingCsvDir, chunksize=chunkSize)
        sql = "INSERT INTO ratings (userId, animeId, rating) VALUES (%s, %s, %s)"

        for df in tqdm(dfs):
            # print(df)
            # df["my_score"] = df["my_score"].fillna(0)
            # df["my_score"] = df["my_score"]+1
            df = df.dropna(subset=["userId","animeId","rating"])

            self.mycursor.executemany(sql, df[["userId","animeId","rating"]].values.tolist())
            self.mydb.commit()

    def dropTable(self, tableName):
        sql = f"DROP TABLE IF EXISTS {tableName}"
        self.mycursor.execute(sql)
        self.mydb.commit()

    def disconnect(self):
        self.mycursor.close()
        self.mydb.close()

    def getRatedAnime(self, userId):
        sql = "SELECT animeId, rating FROM ratings WHERE userId = %s"
        self.mycursor.execute(sql, (userId,))
        result = self.mycursor.fetchall()

        animeIds = []
        ratings = np.zeros(len(result))

        cntr = 0
        for animeId, rating in result:
            animeIds.append(animeId)
            ratings[cntr] = float(rating)
            cntr += 1
        return animeIds, ratings

    def getAverageAnimeRating(self, animeId):
        sql = "SELECT rating FROM ratings WHERE animeId = %s"
        self.mycursor.execute(sql, (animeId,))
        result = self.mycursor.fetchall()

        ratings = np.zeros(len(result))

        cntr = 0
        for rating in result:
            ratings[cntr] = float(rating[0])
            cntr += 1
        return np.mean(ratings)

    def getAverageUserRating(self, userId):
        #Not needed during ALS, but added function for potential future needs
        sql = "SELECT rating FROM ratings WHERE userId = %s"
        self.mycursor.execute(sql, (userId,))
        result = self.mycursor.fetchall()

        ratings = np.zeros(len(result))

        cntr = 0
        for rating in result:
            ratings[cntr] = float(rating[0])
            cntr += 1
        return np.mean(ratings)

    def getRatedUser(self, animeId):
        sql = "SELECT userId, rating FROM ratings WHERE animeId = %s"
        self.mycursor.execute(sql, (animeId,))
        result = self.mycursor.fetchall()

        userIds = []
        ratings = np.zeros(len(result))

        cntr = 0
        for userId, rating in result:
            userIds.append(userId)
            ratings[cntr] = float(rating)
            cntr += 1
        return userIds, ratings

    def getUserALSFeatures(self, userId):
        animeIds, ratings = self.getRatedAnime(userId)

        if ratings.size > 0:
            animeSubmatrix = np.stack([pickle.load(open(f"{self.animeVectorDir}/{animeId}.pckl","rb")) for animeId in animeIds])
        else:
            animeSubmatrix = None
        return animeSubmatrix, ratings

    def getAnimeALSFeatures(self, animeId):
        userIds, ratings = self.getRatedUser(animeId)

        if ratings.size > 0:
            userSubmatrix = np.stack([pickle.load(open(f"{self.userVectorDir}/{userId}.pckl","rb")) for userId in userIds])
        else:
            userSubmatrix = None
        return userSubmatrix, ratings

    def storeUserFeature(self, userId, vector):
        pickle.dump(vector, open("{}/{}.pckl".format(self.userVectorDir, userId), "wb"))

    def storeAnimeFeature(self, animeId, vector):
        pickle.dump(vector, open("{}/{}.pckl".format(self.animeVectorDir, animeId), "wb"))

    def getUserList(self):
        sql = "SELECT uid FROM users"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result

    def getAnimeList(self):
        sql = "SELECT aid FROM animes"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        return result

    def createDirectory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def formatDirectory(self, directory):
        if os.path.exists(directory):
            filelist = [ f for f in os.listdir(directory) if f.endswith(".pckl") ]
            for f in filelist:
                os.remove(os.path.join(directory, f))

    def formatUserVectorCache(self):
        self.formatDirectory(self.userVectorDir)

    def formatAnimeVectorCache(self):
        self.formatDirectory(self.animeVectorDir)

    def cacheUserVector(self):
        #We don't need to initialize user vector during ALS
        self.createDirectory(self.userVectorDir)
        users = self.getUserList()

        idx = 0
        for userId in tqdm(users):
            vector = np.random.uniform(low=-np.sqrt(3.0/self.dims), high=np.sqrt(3.0/self.dims), size=self.dims)
            pickle.dump(vector, open("{}/{}.pckl".format(self.userVectorDir, userId[0]), "wb"))
            idx+=1

    def cacheAnimeVector(self):
        self.createDirectory(self.animeVectorDir)
        animes = self.getAnimeList()

        idx = 0
        for animeId in tqdm(animes):
            avgRating = self.getAverageAnimeRating(animeId[0])
            vector = np.random.uniform(low=-np.sqrt(3.0/self.dims), high=np.sqrt(3.0/self.dims), size=self.dims)
            vector[0] = avgRating
            pickle.dump(vector, open("{}/{}.pckl".format(self.animeVectorDir, animeId[0]), "wb"))
            idx+=1

def debug():
    dbManager = UserAnimeDatabase()
    try:
        # dbManager.initialize("UserList.csv", "anime_cleaned.csv", "curatedRatings.csv")

        # users = dbManager.getAnimeList()
        # for user in users:
        #     print(user[0])
        #     animeIds, ratings = dbManager.getRatedUser(user[0])
        #     print(ratings)
        # dbManager.cacheUserVector()
        # dbManager.cacheAnimeVector()
        # dbManager.formatUserVectorCache()
        dbManager.formatAnimeVectorCache()
        # dbManager.cacheUserVector()
        dbManager.cacheAnimeVector()
        subMatrix, ratings = dbManager.getUserALSFeatures(1)
        print(subMatrix)

        dbManager.disconnect()
    except:
        print("somethings wrong")
        dbManager.disconnect()
# dbManager.dropTable("ratings")
# dbManager.createUserAnimeTable()
# dbManager.insertUserAnimeRating()
# dbManager.getRatedAnime("Warbec")

# userVectors = np.random.normal(scale=np.sqrt(128),size=(100000, 128))
# vectors = [vector.tostring() for vector in userVectors]
# print(len(vectors))

