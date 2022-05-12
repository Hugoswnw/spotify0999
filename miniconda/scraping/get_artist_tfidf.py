import pandas
from neo4j import GraphDatabase
import json
import os
from IPython.display import display

from core.spotify_graph import *


artist = os.environ.get('ARTIST')
if artist:
    uri = "bolt://database:7687"
    with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session() as session:
            res = artist_tfidf_neighbors(session, artist)
            for k, v in res.items():
                print(k, v)
else:
    print("ARTIST not defined, use : ARTIST=<artist> docker-compose tfidf")