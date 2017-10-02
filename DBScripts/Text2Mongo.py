#!/usr/bin/env python3
# -*- coding: iso-8859-9 -*-

import os
from pymongo import MongoClient
from pymongo import ReturnDocument


def getNextSequenceValue(sequenceName, counters):

   sequenceDocument = counters.find_one_and_update(
      {"_id": sequenceName },
      {"$inc":{"sequence_value": 1}},
       return_document=ReturnDocument.AFTER
      #{"done": True}
   );
   return sequenceDocument["sequence_value"];

client = MongoClient('mongodb://testuser:testuser@ds151014.mlab.com:51014/nlpdatabase')

db = client.get_database("nlpdatabase")
counters = db.get_collection("counters")
counters.update({"_id" : "docId"}, {"$set": { "sequence_value" : 0}})
#counters.insert({"_id":"docId", "sequence_value": 0})
news = db.get_collection("news")
news.remove({})
#mainDirectory = "/Users/mcangny/Downloads/1150haber/raw_texts/"
mainDirectory = current_dir = os.path.abspath(os.path.dirname(__file__))
mainDirectory = mainDirectory + "/1150haber/raw_texts/"

categories = next(os.walk(mainDirectory))[1]

news2insert = []

for cat in categories:
    files = next(os.walk(mainDirectory + cat))[2]
    for file in files:
        with open(mainDirectory + cat + "/" + file, 'r', encoding='iso-8859-9') as content_file:
            content = content_file.read()
            news2insert.append({
                "_id": getNextSequenceValue("docId", counters),
                "filename": file,
                "text": content,
                "class": cat
            })


result = news.insert(news2insert)









