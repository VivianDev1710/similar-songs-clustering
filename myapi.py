from fastapi import FastAPI, Path
# from typing import Optional
# from pydantic import BaseModel
import pandas as pd
import numpy as np
import sklearn
# from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import KMeans

#clean the data
df=pd.read_csv("genres_v2.csv")
new_df = df.loc[:, ['id','track_href','song_name','danceability', 'energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]
clean_df=new_df.dropna()
clean_df=clean_df.drop_duplicates()

#cluster the data initially
X=clean_df[['danceability', 'energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]
kmeans = KMeans(n_clusters=6)
kmeans.fit(X)
labels = kmeans.labels_
clean_df['cluster'] = labels


app=FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-songs/{start}")
def get_songs(start: int):
    print(clean_df.shape)
    data = clean_df[['id', 'song_name']][start:start+100]
    print(data.shape)
    # data = clean_df.iloc[100:200][['id', 'song_name']]
    response = []
    for i in range(100):
        response.append([data['id'][start+i],data["song_name"][start+i]])

    # Convert the selected data to a JSON format
    # json_data = data.to_json(orient='records')
    # # Return the JSON data
    return response

@app.post("/like-song/{song_id}")
def like_song(song_id: str):
    with open("liked.txt", "r") as file:
        lines = file.readlines()
    lines = list(map(lambda x: x[:-1], lines))
    if song_id in  lines:
        print('found')
        return {"id":"liked"}
    with open('liked.txt', 'a') as f:
        f.write(song_id+'\n')
    return {"id":"liked"}

@app.post("/unlike-song/{song_id}")
def like_song(song_id: str):
    with open("liked.txt", "r") as file:
        lines = file.readlines()
    lines = list(map(lambda x: x[:-1], lines))
    new_lines = [line+"\n" for line in lines if line.strip() != song_id]
    with open("liked.txt", "w") as file:
        file.writelines(new_lines)

@app.get("/get-simm/{song_id}")
def get_simm(song_id: str):
    with open("liked.txt", "r") as file:
        lines = file.readlines()
    liked = list(map(lambda x: x[:-1], lines))
    liked_df = clean_df[clean_df['id'].isin(liked)]
    [a,b]=liked_df['cluster'].value_counts().nlargest(2).index.tolist()
    new_df = clean_df[(clean_df['cluster'] == a) | (clean_df['cluster'] == b)]
    row_to_add = clean_df[clean_df['id'] == song_id]
    new_df = new_df.append(row_to_add)
    new_df=new_df.drop_duplicates()

    X=new_df[['danceability', 'energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]
    kmeans = KMeans(n_clusters=new_df.shape[0]//300)
    kmeans.fit(X)
    labels = kmeans.labels_
    new_df['cluster'] = labels
    cluster_value = new_df.loc[new_df['id'] == song_id, 'cluster'].values[0]
    simm_df=new_df[new_df['cluster'] == cluster_value]
    
    data = simm_df[['id', 'song_name']][0:100]
    print(2)
    response = []
    print(data)
    for i in range(100):
        response.append([data.iloc[i]['id'],data.iloc[i]["song_name"]])
    print(1)
    return response

