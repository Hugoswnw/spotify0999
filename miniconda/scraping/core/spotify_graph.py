def match_playlist(tx, pid, name, followers):
    return tx.run("""
        MERGE (:Playlist {pid: $pid, name: $name, followers: toInteger($followers)})
    """, pid=pid, name=name, followers=followers)

def match_artist(tx, uri, name):
    return tx.run("""
        MERGE (:Artist {uri: $uri, name: $name})
    """, uri=uri, name=name)

def match_album(tx, uri, name):
    return tx.run("""
        MERGE (:Album {uri: $uri, name: $name})
    """, uri=uri, name=name)

def match_track(tx, uri, name, duration):
    return tx.run("""
        MERGE (:Track {uri: $uri, name: $name, msDuration: toInteger($duration)})
    """, uri=uri, name=name, duration=duration)

def merge_link_artist_album(tx, artist_uri, album_uri):
    return tx.run("""
        MATCH (artist:Artist {uri: $artist_uri}), (album:Album {uri: $album_uri}) 
        MERGE (artist)-[:CREATED]->(album)
    """, artist_uri=artist_uri, album_uri=album_uri)

def merge_link_album_track(tx, album_uri, track_uri):
    return tx.run("""
        MATCH (album:Album {uri: $album_uri}), (track:Track {uri: $track_uri}) 
        MERGE (album)-[:CONTAINS]->(track)
    """, album_uri=album_uri, track_uri=track_uri)

def merge_link_playlist_track(tx, playlist_pid, track_uri):
    return tx.run("""
        MATCH (playlist:Playlist {pid: $playlist_pid}), (track:Track {uri: $track_uri}) 
        MERGE (playlist)-[:CONTAINS]->(track)
    """, playlist_pid=playlist_pid, track_uri=track_uri)

def get_coplaylist_artist_counts(tx, artist_partial_name):
    return tx.run("""
        MATCH (n:Artist)--(:Album)--(:Track)--(p:Playlist), 
        (m:Artist)--(:Album)--(:Track)--(p:Playlist) 
        WHERE n.name CONTAINS "Arctic" 
        RETURN m.name, count(m) 
        ORDER BY count(m) DESC
    """, playlist_pid=playlist_pid, track_uri=track_uri)