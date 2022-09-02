from neo4j import GraphDatabase
import pandas as pd
import numpy as np
from core.neo4j.get import get_featuring_artists
from core.neo4j.merge import *
from core.spotify_scraping import *

def query_merge_artist_tracks(artist_id):
    with GraphDatabase.driver("bolt://database:7687", auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session() as session:
            albums = query_artist_albums(token, artist_id)
            for album in albums:
                merge_entity(session, "Album", **{k : album[k] for k in ['album_type', 'available_markets', 'id', 'name', 'release_date', 'uri']})
                tracks = query_album_tracks(token, album["id"])
                for track in tracks:
                    merge_entity(session, "Track", **{k : track[k] for k in ['duration_ms', 'explicit', 'id', 'name', 'uri']})
                    merge_link_album_track(session, album["uri"], track["uri"])
                    for a in track["artists"]:
                        merge_entity(session, "Artist", **{k : track[k] for k in ['id', 'name', 'uri']})
                        merge_link_artist_track(session, a["uri"], track["uri"])
            merge_artist_update_date(session, artist_id)


client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

score = lambda d, t : 1 + ( 1 +np.e**-(d/10 + (1-(t/(2**16)))))**10
artist_id = "3DCWeG2J1fZeu0Oe6i5Q6m"
distance = 0
artists = pd.DataFrame()
while True:
    token = request_token(client_id, client_secret)
    with GraphDatabase.driver("bolt://database:7687", auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session() as session:
            feat_artists = get_featuring_artists(session, artist_id)
            feat_artists["distance"] += distance
            artists = pd.concat([artists, feat_artists])
            del feat_artists

    artists = artists.groupby("id").min().reset_index()
    artists["score"] = artists.apply(lambda x : score(x["distance"], x["last_update"]), axis=1)
    artist = artists.sample(n=1, weights="score").iloc[0]
    artist_id, distance = artist["id"], artist["distance"]
    print(artist["name"])
    try:
        query_merge_artist_tracks(artist_id)
    except Exception as e:
        print(e)