import random
import os
import scipy.spatial as sp
from gensim.models import Doc2Vec
from pymongo import MongoClient


#get already trained model
def get_model():

    dir = current_dir = os.path.abspath(os.path.dirname(__file__))
    #get model
    model = Doc2Vec.load(dir + "/doc2vec.bin")
    #get data from db
    client = MongoClient('mongodb://testuser:testuser@ds151014.mlab.com:51014/nlpdatabase')
    db = client.get_database("nlpdatabase")
    news = db.get_collection("news")
    #get 10 random numbers
    numbers = random.sample(range(1, 1150), 10)
    texts = []
    #get text data from db
    texts = list(news.find({"_id": {"$in": numbers}}))
    data = []

    for i in range(1, len(numbers) - 1):
        for j in range(i + 1, len(numbers) - 1):
            result = 1 - sp.distance.cosine(model.docvecs[str(numbers[i])], model.docvecs[str(numbers[j])])
            #print("cousine similarity between " + str(numbers[i]) + " and " + str(numbers[j]) + " = " + str(result))
            text1 = [item for item in texts if item["_id"] == numbers[i]]
            text1_id = text1[0]["_id"]
            text1_text = text1[0]["text"]
            text1_filename = text1[0]["filename"]
            #print(str(numbers[i]) + " " + text1[0]["class"])
            text2 = [item for item in texts if item["_id"] == numbers[j]]
            text2_id = text2[0]["_id"]
            text2_text = text2[0]["text"]
            text2_filename = text2[0]["filename"]

            #print(str(numbers[j]) + " " + text2[0]["class"])

            comparison_data = {
                "result": result,
                "textids": [text1_id, text2_id],
                "texts_filename" : [text1_filename, text2_filename],
                "text1": text1_text,
                "text2": text2_text
            }

            data.append(comparison_data)
    return data

