import re
from pymongo import MongoClient
import random
import json


class RemoteIO:
    def __init__(self):
        self.db = MongoClient('njuse', 30000).get_database("lawCase").get_collection('paragraph')

    def read_from_remote(self):
        db = self.db
        return db.find({}, {"plaintiffAlleges": 1, "defendantArgued": 1})


class CorpusIO:
    def __init__(self):
        self.db = None

    def fetch_sentences_from_remote(self, limit=1000):
        cursor = RemoteIO().read_from_remote()
        stc_db = MongoClient('localhost', 27017).get_database(
            'judgement').get_collection('sentences_' + str(limit))

        count = limit
        for doc in cursor:
            if count < 0:
                break

            pa = doc["plaintiffAlleges"]
            da = doc["defendantArgued"]
            if re.match(r"d+$", pa) and re.match(r"d+$", da):
                # is figure, pass
                pass
            else:
                count -= 1
                pa_segs = re.split('。?？；：，;:,', pa)
                da_segs = re.split('。；：？?，;:,', da)
                for seg in pa_segs:
                    stc_db.save({"text": seg})
                for seg in da_segs:
                    stc_db.save({"text": seg})

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
