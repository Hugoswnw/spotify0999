from neo4j import GraphDatabase
import json
import os

from core.neo4j.get import *

uri = "bolt://database:7687"
entities = ["Artist", "Album", "Track", "Playlist"]
with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
    with driver.session(database="neo4j") as session:
        for entity in entities:
            res = session.read_transaction(get_entity_count, entity)
            print(f"{entity}s : {res}")

        for a in entities:
            for b in entities:
                if a != b:
                    res = session.read_transaction(get_entities_edge_count, a, b)
                    print(f"{a}s -- {b}s : {res}")