import pandas
from neo4j import GraphDatabase
import json
import pandas as pd
import numpy as np
from zipfile import ZipFile
import re
import os, sys

from core.neo4j.merge import *

uri = "bolt://database:7687/"
regex = re.compile("data.*\.json")
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    with ZipFile(os.path.join("data", "spotify_million_playlist_dataset.zip")) as zip_file:
        slices = [f for f in zip_file.namelist() if regex.match(f)]
        for slice_path in slices:
            with zip_file.open(slice_path) as raw_playlist:
                with driver.session(database="neo4j") as session:
                    print(slice_path)
                    playlists = json.loads(raw_playlist.read())
                    for playlist in playlists["playlists"]:
                        playlist_uri = f"dump:spotify:{playlist['pid']}"
                        merge_entity(session, "Playlist", id=playlist['pid'], name=playlist['name'],
                                num_followers=playlist['num_followers'], uri=playlist_uri)
                        for track in playlist['tracks']:
                            merge_entity(session, "Artist", uri=track["artist_uri"],
                                name=track["artist_name"], id=track["artist_name"].split(":")[-1])
                            merge_entity(session, "Album", uri=track["album_uri"],
                                name=track["album_name"], id=track["album_uri"].split(":")[-1])
                            merge_entity(session, "Track", uri=track["track_uri"], name=track["track_name"],
                                duration_ms=track["duration_ms"], id=track["album_uri"].split(":")[-1])

                            merge_link_artist_track(session, track["artist_uri"], track["track_uri"])
                            merge_link_album_track(session, track["album_uri"], track["track_uri"])
                            merge_link_playlist_track(session, playlist_uri, track["track_uri"])
