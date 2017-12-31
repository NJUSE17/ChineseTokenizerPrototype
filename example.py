import json

from Network import CorpusGraph
from Network import TextGraph
from ResultReference import JiebaChecker
from ResultReference import ThulacChecker

cg = CorpusGraph()
# cg.build_corpus()
# cg.save_as_json('./data/ten.json')
cg.load_from_json('./data/two.json')
jieba_checker = JiebaChecker()
thulac_checker = ThulacChecker()

def tokenize(sentence):
    tg = TextGraph()
    tg.build([sentence])
    tg.fill_edge(cg)

    # 暂时只对单句分词
    result = tg.cut()[0]
    jieba_check = jieba_checker.check(sentence, result)
    thulac_check = thulac_checker.check(sentence, result)

    jieba_result = jieba_check["jieba_result"]
    jieba_overlap = jieba_check["overlap"]

    thulac_result = thulac_check["thulac_result"]
    thulac_overlap = thulac_check["overlap"]
    res = json.dumps(
        {"result": result, "jieba": jieba_result, "jieba_overlap": jieba_overlap,"thulac":thulac_result,"thulac_overlap":thulac_overlap},
        ensure_ascii=False)
    return res

print(tokenize("被告章卫平归还原告借款本金9000元"))