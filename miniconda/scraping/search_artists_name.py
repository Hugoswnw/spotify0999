import pandas
from neo4j import GraphDatabase
import json
import os

from core.spotify_graph import *


artist = os.environ.get('ARTIST')
if artist:
    uri = "bolt://database:7687"
    with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session() as session:
            res = session.read_transaction(search_entity_names, "Artist", artist)
            print("\n".join(res))
else:
    print("ARTIST not defined, use : ARTIST=<artist> docker-compose search-name")