from neo4j import GraphDatabase

from core.neo4j.get import *


def artist_tfidf(artist_name, idf=.5, reverse=True):
    uri = "bolt://database:7687"
    with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session() as session:
            res = get_coplaylist_artist_counts(session, artist_name)
            counts = get_artists_total_playlist_counts(session, res.keys())
            score = {artist: co_occ / counts[artist] ** idf for artist, co_occ in res.items()}
            return {k: v for k, v in sorted(score.items(), key=lambda x: x[1], reverse=reverse)}
