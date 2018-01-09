import re
from pymongo import MongoClient
import random
import json


class RemoteIO:
    def __init__(self):
        self.db = MongoClient('192.168.68.11', 20000).get_database("tokenizer_qiao").get_collection('sentences_splited')
        self.sentence_size = self.db.find().count()
        self.step = self.sentence_size
        self.skip = 0

    def read_sentence_randomly(self):
        while self.skip + self.step >= self.sentence_size:
            self.skip = 0
            self.step = int(self.step/2)
        if self.step + self.skip < self.sentence_size:
            random_step = random.randint(0, self.step)
            pipeline = [
                {"$skip": self.skip+random_step},
                {"$limit": 1}
            ]
            self.skip += random_step
            docs = list(self.db.aggregate(pipeline))
            doc = docs[0] if len(docs) > 0 else None
            self.db.update({"_id": doc["_id"]}, {"$inc": {"analysed": 1}})
            return doc
        else:
            return None

    def read_sentence_from_remote(self):
        db = self.db
        return db.find()


class CorpusIO:
    def __init__(self):
        self.db = None

    # 从数据库构造语料库
    def read_from_mongo(self, limit=20):
        db = self.db if self.db is not None else MongoClient('localhost', 27017).get_database(
            'edges').get_collection('t_t')
        cursor = db.find({})
        cnt = 0
        for doc in cursor:
            if limit is not None and cnt > limit:
                break
            cnt += 1
            if cnt % 10000 == 0:
                print(cnt)
            edge = (doc['src'], doc['des'], doc['weight'])
            yield edge

    def save_as_json(self, corpus_json, path):
        file = open(path, 'w', encoding='utf-8')
        json.dump(corpus_json, file, ensure_ascii=False)
        print('corpus network saved to %s' % path)

    def load_as_json(self, path):
        file = open(path, 'r', encoding='utf-8')
        corpus_json = json.load(file)
        return corpus_json


class TextIO:
    def __init__(self):
        self.db = MongoClient('localhost', 27017).get_database('chinese').get_collection('train')

    def get_mongo_size(self):
        size = self.db.count()
        # print("size: %d" % size)
        return size

    def get_text_from_mongo(self, skip=0, limit=1, isRandom=True):
        size = self.get_mongo_size()
        if isRandom:
            skip = random.randint(0, size - limit)

        cursor = self.db.find().skip(skip).limit(limit)
        for doc in cursor:
            yield doc['text']


class DisIO:
    def __init__(self):
        self.db = MongoClient('localhost', 27017).get_database('orig').get_collection('sentences')

    def sen_from_mongo(self):
        cursor = self.db.find({})
        str = ""
        for sen in cursor:
            str = str + sen['text']
        return str

    def re_to_text(self, path, cut=[]):
        jieba_sum = 0.0
        thulac_sum = 0.0
        dis = open(path, 'a', encoding='utf-8')
        length = len(cut)
        for i in range(0, length):
            jieba_sum += cut[i]["jieba_overlap"]
            thulac_sum += cut[i]["thulac_overlap"]
            dis.write("origin: " + cut[i]["sentence"] + "\n")
            dis.write("result: " + str(cut[i]["result"]) + "\n")
            dis.write("jieba:  " + str(cut[i]["jieba"]) + "  " + str(cut[i]["jieba_overlap"]) + "\n")
            dis.write("thulac: " + str(cut[i]["thulac"]) + "  " + str(cut[i]["thulac_overlap"]) + "\n\n")
        dis.write(
            "jieba:" + "n/a" if length == 0 else str(jieba_sum / length) + "  thulac:" + "n/a" if length == 0 else str(
                thulac_sum / length) + "\n")
        dis.close()
