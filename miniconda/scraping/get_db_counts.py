import pandas
from neo4j import GraphDatabase
import json
import os
from IPython.display import display

from core.spotify_graph import *

uri = "bolt://database:7687"
entities = ["Artist", "Album", "Track", "Playlist"]
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    for entity in entities:
        with driver.session() as session:
            res = session.read_transaction(get_entity_count, entity)
            print(f"{entity}s : {res}")