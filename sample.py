import json

from Network import CorpusGraph
from Network import TextGraph
from ResultReference import JiebaChecker

cg = CorpusGraph()
cg.load_from_json()
checker = JiebaChecker()

def tokenize(sentence):
    tg = TextGraph()
    tg.build([sentence])
    tg.fill_edge(cg)

    # 暂时只对单句分词
    result = tg.cut()[0]
    check = checker.check(sentence, result)

    jieba_result = check["jieba_result"]
    overlap = check["overlap"]
    res = json.dumps(
        {"result": result, "jieba": jieba_result, "overlap": overlap},
        ensure_ascii=False)
    return res

print(tokenize("原告已履行退款义务的银行卡及汇款凭证等证据"))