def merge_entity(tx, entity_name, **props):
    props = {k: v for k, v in props.items() if v is not None}
    added_keys = ", ".join([f"{k}: ${k}" for k in props.keys()])
    return tx.run("MERGE (: " + entity_name + " {" + added_keys + "})", **props)


def merge_link_playlist_track(tx, playlist_uri, track_uri):
    return tx.run("""
        MATCH (playlist:Playlist {uri: $playlist_uri}), (track:Track {uri: $track_uri})
        MERGE (playlist)-[:CONTAINS]->(track)
    """, playlist_uri=playlist_uri, track_uri=track_uri)


def merge_link_artist_track(tx, artist_uri, track_uri):
    return tx.run("""
        MATCH (artist:Artist {uri: $artist_uri}), (track:Track {uri: $track_uri})
        MERGE (artist)-[:CREATED]->(track)
    """, artist_uri=artist_uri, track_uri=track_uri)


def merge_link_album_track(tx, album_uri, track_uri):
    return tx.run("""
        MATCH (album:Album {uri: $album_uri}), (track:Track {uri: $track_uri})
        MERGE (album)-[:CONTAINS]->(track)
    """, album_uri=album_uri, track_uri=track_uri)
