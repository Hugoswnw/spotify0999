import os

from core.neo4j.get import get_playlists_uri
from core.neo4j.merge import *
from core.spotify_scraping import request_token, search_playlists, query_playlist_tracks
from neo4j import GraphDatabase
from time import sleep
import pandas as pd


client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

uri = "bolt://database:7687"
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    with driver.session() as session:
        for genre in pd.read_csv("scraping/ressources/playlist_keywords.txt", header=None)[0]:
            token = request_token(client_id, client_secret)
            playlists = search_playlists(token, genre, limit=500)
            stored_playlist_uris = get_playlists_uri(session)


            for playlist in playlists:
                if playlist["uri"] in stored_playlist_uris:
                    #print(playlist["name"], "skipped!")
                    continue

                token = request_token(client_id, client_secret)
                print(playlist["name"])
                playlist_tracks = query_playlist_tracks(token, playlist["id"])

                merge_entity(session, "Playlist", **{k : playlist[k] for k in ['description', 'id', "uri", 'name']})
                for track in playlist_tracks["items"]:
                    if not "track" in track.keys():
                        print("track ignored")
                        continue

                    for artist in track["track"]["artists"]:
                        try:
                            merge_entity(session, "Artist", **{k : artist[k] for k in ['id', 'name', 'uri']})
                            merge_link_artist_track(session, artist["uri"], track["track"]["uri"])
                        except Exception as e:
                            print(e)

                    try:
                        album = track["track"]["album"]
                        merge_entity(session, "Album", **{k : album[k] for k in ['album_type', 'id', 'name', 'uri', 'release_date']})
                        merge_link_album_track(session, album["uri"], track["track"]["uri"])
                    except Exception as e:
                        print(e)

                    try:
                        merge_entity(session, "Track", **{k : track["track"][k] for k in ['duration_ms', 'explicit', 'id', 'name', 'uri', 'popularity']})
                        merge_link_playlist_track(session, playlist["uri"], track["track"]["uri"])
                    except Exception as e:
                        print(e)

            sleep(.1)