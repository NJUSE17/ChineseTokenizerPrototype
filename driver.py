import jieba
import re

from IO import CorpusIO
from IO import TextIO
# from Network import CorpusGraph
# from Network import TextGraph
from Graph import CorpusGraph
from Graph import TextGraph
from utl import count as time_count


def test_text():
    cg = CorpusGraph()

    # 从json文件读取语料库模型
    cg.load_from_json()

    # 连接mongodb建立语料库模型
    # cg.build_corpus()

    # 保存为json文件
    # cg.save_as_json()

    tg = TextGraph()

    # 从mongodb读取句子，以便分词
    # sentences = tg.get_sentences(isRandom=False, limit=10)

    sentences = ["准许原告肖振明撤回起诉", "这是第二个句子的测试", "第三个橘子"]

    # 对句子数组建立图模型
    tg.build(sentences, cg)

    # 填入边的权重
    tg.fill_edge(cg)

    # 输出语句图需要的json文件, path如果为None则返回json，而不保存在硬盘
    # tg.make_json(cg, path='./data/text.json')

    #
    rs = tg.cut()
    return rs


# test_text()
def make_local_mongo():
    corpusio = CorpusIO()
    # corpusio.fetch_sentences_from_remote()


# 与jieba对比时间开销
def compare_time_cost(size):
    list(jieba.cut("先加载词典"))
    time_count("init", print_to_console=False)

    sentences = TextIO().get_text_from_mongo(isRandom=False, limit=size)

    # time_count("get sentences")

    cg = CorpusGraph()
    cg.load_from_json()
    # cg.cache_reverse()
    time_count("build corpus graph")

    tg = TextGraph()
    tg.build(sentences, cg)
    time_count(print_to_console=False)
    # tg.fill_edge(cg)
    # time_count("fill edge")
    rs = tg.cut()
    time_count("time cost")
    # print(rs)

    # sentences 是生成器，上面的sentences已经被消耗
    sentences = TextIO().get_text_from_mongo(isRandom=False, limit=size)
    jieba_rs = []
    time_count(print_to_console=False)

    for s in sentences:
        words_gen = jieba.cut(s)
        words = list(words_gen)
        jieba_rs.append(words)

    time_count("jieba time cost")


compare_time_cost(100000)
# rs = test_text()
# print(rs)