def get_coplaylist_artist_counts(tx, artist_partial_name):
    res = tx.run(
        f'MATCH (u:Artist)--(:Track)--(:Playlist)--(:Track)--(v:Artist) WHERE u.name CONTAINS "{artist_partial_name}" RETURN v.name, count(*)')
    return {artist: count for artist, count in res}


def get_artists_total_playlist_counts(tx, artists):
    q = f"MATCH (u:Artist)--(t:Track)--(p:Playlist) WHERE u.name IN {str(list(artists))} RETURN u.name, count(DISTINCT p.name)"
    res = tx.run(q)
    return {artist: count for artist, count in res}


def get_playlists_uri(tx):
    return [uri[0] for uri in tx.run("MATCH (p:Playlist) RETURN p.uri").values()]


def get_entities_edge_count(tx, entity_a, entity_b):
    res = tx.run(f"""
        MATCH (:{entity_a})-[e]-(:{entity_b})
        RETURN count(e) as count
    """)
    return res.single()["count"]


def get_entity_count(tx, entity):
    res = tx.run(f"""
        MATCH (:{entity})
        RETURN count(*) as count
    """)
    return res.single()["count"]


def get_entity_names(tx, entity, name):
    res = tx.run(f"""
        MATCH (n:{entity})
        WHERE toLower(n.name) CONTAINS '{name.lower()}'
        RETURN n.name as name
    """)
    return [r["name"] for r in res]

