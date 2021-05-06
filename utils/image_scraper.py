import pandas as pd
import requests
import os
import shutil
from tqdm import tqdm

CSV_PATH = 'data/AnimeImages.csv'
DIR_PATH = 'data/images/{directory}'

df = pd.read_csv(CSV_PATH)
cols = ['anime_id', 'images']
data = pd.DataFrame(df, columns=cols)
# remove bad rows
data = data.loc[data['images'] != 'set()']
data = data.loc[data['images'] != 'N/A']
data = data.dropna()

for i in tqdm(range(len(data.index))):
    anime_id = data.iloc[i]['anime_id']
    images = data.iloc[i]['images']

    try:
        images = images.replace('{', '').replace(
            '}', '').replace(' ', '').replace("'", '').split(',')

        try:
            os.makedirs(DIR_PATH.format(directory=anime_id))
        except FileExistsError:
            # directory already exists
            pass

        for image_url in images:
            filename = image_url.split("/")[-1]
            response = requests.get(image_url, stream=True)

            if response.status_code == 200:
                response.raw.decode_content = True

                filename = os.path.join(
                    DIR_PATH.format(directory=anime_id), filename)

                with open(filename, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)

                # print('Image sucessfully Downloaded: ', filename)
            else:
                print('Image for {anime_id} could not be downloaded: {file}'.format(anime_id=anime_id, file=filename))
    except:
        print('Error with {anime_id} downloading {images}'.format(
            anime_id=anime_id, images=images))
