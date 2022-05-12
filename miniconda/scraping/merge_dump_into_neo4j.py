import pandas
from neo4j import GraphDatabase
import json
import pandas as pd
import numpy as np
from zipfile import ZipFile
import re
import os, sys

from core.spotify_graph import *

slices = os.listdir(json_src)
uri = "bolt://database:7687/"
regex = re.compile("data.*\.json")
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    with ZipFile(os.path.join("data", "spotify_million_playlist_dataset.zip")) as zip_file:
        slices = [f for f in zip_file.namelist() if regex.match(f)]
        for slice_path in slices:
            with zip_file.open(slice_path) as raw_playlist:
                print(slice_path)
                playlists = json.loads(raw_playlist.read())
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