from neo4j import GraphDatabase
import json
import os

from core.legacy_spotify_graph import search_entity_names

artist = os.environ.get('ARTIST')
if artist:
    uri = "bolt://database:7687"
    with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session(database="neo4j") as session:
            res = session.read_transaction(search_entity_names, "Artist", artist)
            print("\n".join(res))
else:
    print("ARTIST not defined, use : ARTIST=<artist> docker-compose search-name")