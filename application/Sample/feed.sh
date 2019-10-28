#!/usr/bin/env bash

mongod --version

echo test mongo shell commands
mongo test --eval "printjson(db.getCollectionNames())"

echo Refresh collections
mongo --eval "
    db = db.getSiblingDB('soccerdb');
    db.getCollectionNames();
    db.matchinfos.drop();
"

echo Refill collections with sample data
mongoimport --jsonArray --db soccerdb --collection matchinfos --file sample.json
