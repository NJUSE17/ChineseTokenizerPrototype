from Network import CorpusGraph
from Network import TextGraph

def make_corpus():
    cg = CorpusGraph()
    cg.build_corpus()
    # cg.save_as_json()
    cg.load_from_json()
    # cg.draw()


def test_text():
    cg = CorpusGraph()
    # cg.load_from_json()
    cg.build_corpus()
    cg.save_as_json()
    # cg.get_sorted_neighbour('一')
    # print("###############")
    # for cge in cg.corpus.edges:
    #     print(cge)
        # break
    # print('###', cg.corpus['朝'])

    tg = TextGraph()
    # sentences = tg.get_sentences(isRandom=False)
    sentences = ["准许原告肖振明撤回起诉"]
    tg.build(sentences)
    tg.fill_edge(cg)
    tg.make_json(cg)

test_text()