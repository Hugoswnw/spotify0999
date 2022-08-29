import base64
import os
from datetime import datetime
import requests as requests
import json


def request_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

    headers['Authorization'] = f"Basic {message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)
    return r.json()["access_token"]


def query(token, url, data=None, params=None, keep_track=None):
    if params is None:
        params = {}
    if data is None:
        data = {}
    headers = {}
    headers['Authorization'] = f"Bearer {token}"
    headers['Content-Type'] = f"application/json"

    r = requests.get(url, headers=headers, data=data, params={k: v for k, v in params.items() if v is not None})

    if keep_track:
        with open(os.path.join(keep_track, datetime.now().strftime("%H:%M:%S-%d.%m.%Y.json")), "w") as o:
            json.dump({"query": {"url": url, "headers": headers, "params": params, "data": data}, "response": r.json()},
                      o)
    return r.json()


def query_artists(token, artists_id):
    chunk_size = 50
    chunked_artists_ids = [artists_id[x:x + chunk_size] for x in range(0, len(artists_id), chunk_size)]
    for chunk in chunked_artists_ids:
        r = query(token, f"https://api.spotify.com/v1/artists/?ids={','.join(chunk)}")
        for artist in r["artists"]:
            yield artist


def search_playlists(token, keyword, limit=50):
    MAX_LIMIT = 50
    playlists = []
    curr_offset = 0
    while len(playlists) < limit:
        params = {
            "q": keyword,
            "type": "playlist",
            "limit": min(MAX_LIMIT, limit - len(playlists)),
            "offset": curr_offset
        }
        r = query(token, f"https://api.spotify.com/v1/search", params=params)
        for playlist in r["playlists"]['items']:
            playlists.append(playlist)
        curr_offset += MAX_LIMIT
    return playlists


def query_playlist_tracks(token, playlist_id):
    r = query(token, f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks")
    return r