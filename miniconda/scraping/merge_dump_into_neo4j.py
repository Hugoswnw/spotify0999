import pandas
from neo4j import GraphDatabase
import json
import os
from IPython.display import display
from progress.bar import IncrementalBar

from core.spotify_graph import *

json_src = os.path.join("data", "data")
slices = os.listdir(json_src)
uri = "bolt://database:7687"
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    for slice_f in slices:
        with open(os.path.join(json_src, slice_f)) as f:
            print(slice_f)
            playlists = json.load(f)
            for playlist in playlists["playlists"]:
                with driver.session() as session:
                    session.write_transaction(match_playlist, playlist['pid'], playlist['name'], playlist['num_followers'])
                for track in playlist['tracks']:
                    transactions = []
                    transactions.append((match_artist, track["artist_uri"], track["artist_name"]))
                    transactions.append((match_album, track["album_uri"], track["album_name"]))
                    transactions.append((match_track, track["track_uri"], track["track_name"], track["duration_ms"]))
                    transactions.append((merge_link_artist_album, track["artist_uri"], track["album_uri"]))
                    transactions.append((merge_link_album_track, track["album_uri"], track["track_uri"]))
                    transactions.append((merge_link_playlist_track, playlist['pid'], track["track_uri"]))
                    for transactions in transactions:
                        with driver.session() as session:
                            session.write_transaction(*transactions)
        os.remove(os.path.join(json_src, slice_f))