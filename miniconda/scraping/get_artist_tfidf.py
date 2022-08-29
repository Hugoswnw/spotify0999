import pandas
from neo4j import GraphDatabase
import json
import os

from core.neo4j.scores import artist_tfidf

artist = os.environ.get('ARTIST')
if artist:
    uri = "bolt://database:7687"
    with GraphDatabase.driver(uri, auth=("neo4j", "ouiouioui"), encrypted=False) as driver:
        with driver.session(database="neo4j") as session:
            res = artist_tfidf(session, artist)
            for k, v in res.items():
                print(k, v)
else:
    print("ARTIST not defined, use : ARTIST=<artist> docker-compose tfidf")