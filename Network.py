import json

from IO import CorpusIO
from IO import TextIO
import networkx as nx
import matplotlib.pyplot as plt


class CorpusGraph:
    def __init__(self):
        self.corpus = nx.DiGraph()
        self.corpus_io = CorpusIO()

    # 需要mongodb
    def build_corpus(self):
        edges_gen = self.corpus_io.read_from_mongo(limit=None)
        for edge in edges_gen:
            self.corpus.add_edge(edge[0], edge[1], weight=edge[2])

    def draw(self):
        nx.draw_networkx(self.corpus, font_family='SimHei', node_color='white')
        plt.show()

    def to_json(self):
        json_obj = nx.to_dict_of_dicts(self.corpus)
        return json_obj

    def save_as_json(self, path='./data/corpus.json'):
        json_obj = self.to_json()
        self.corpus_io.save_as_json(json_obj, path)

    def load_from_json(self, path='./data/corpus.json'):
        print("loading corpus json file")
        json_obj = self.corpus_io.load_as_json(path)
        print("loaded")
        self.corpus = nx.from_dict_of_dicts(json_obj, create_using=self.corpus)

    def get_edge_weight(self, start, end):
        weight = 0
        try:
            weight = self.corpus[start][end]['weight']
        except KeyError:
            pass
        return weight

    def get_sorted_neighbour(self, key, exclude=None, K=6):
        if key not in self.corpus.adj:
            return []

        nbr = self.corpus.adj[key]
        rs = []
        # print(nbr)
        # ########### 只需要获得前K个最大值，这里的排序可以优化(堆排序/K次冒泡排序...) ####################
        sorted_nbr = sorted(nbr.items(), key=lambda item: item[1]['weight'], reverse=True)

        j = 0
        for i in range(K - 1):
            if j >= len(sorted_nbr):
                break

            # 循环K次，如果相邻字正好是下一个字，则跳过这个相邻字
            if sorted_nbr[j][0] == exclude:
                j += 1
            rs.append((sorted_nbr[j][0], sorted_nbr[j][1]['weight']))
            j += 1

        remain_cnt = 0
        remain_weight = 0
        for i in range(K - 1, len(sorted_nbr)):
            if sorted_nbr[i][0] == exclude:
                continue
            remain_cnt += 1
            remain_weight += sorted_nbr[i][1]['weight']

        rs.append(("+" + str(remain_cnt), remain_weight))
        return rs
        # print(sorted_nbr)


class TextGraph:
    def __init__(self):
        self.text_io = TextIO()
        self.text = nx.DiGraph()
        self.id_char_map = {}
        self.sentence_cnt = 0

    def get_sentences(self, isRandom=True):
        ss = self.text_io.get_text_from_mongo(isRandom=isRandom)
        return ss
        # self.build(ss)

    def build(self, sentences):
        sentence_index = 10000
        for s in sentences:
            s = s.strip()
            s_size = len(s)
            for char_index in range(s_size):
                char = s[char_index]
                id = sentence_index + char_index
                self.text.add_node(id)
                self.id_char_map[id] = char
                if char_index < s_size - 1:
                    self.text.add_edge(id, id + 1)
            sentence_index += 10000

    def fill_edge(self, corpus):
        edges = self.text.edges()
        for edge in edges:
            char_start = self.id_char_map[edge[0]]
            char_end = self.id_char_map[edge[1]]
            weight = corpus.get_edge_weight(char_start, char_end)
            self.text[edge[0]][edge[1]]['weight'] = weight
            # print(char_start, char_end, weight)
            # print(edges)

    def make_json(self, corpus, path='./data/text.json'):
        # edges = self.text.edges()
        text_json = {}
        i = 0
        for start_id, nbr in self.text.adj.items():
            start_char = self.id_char_map[start_id]
            end_char = self.id_char_map[start_id + 1] if start_id + 1 in nbr else None
            out_weight = nbr[start_id + 1]['weight'] if start_id + 1 in nbr else 0
            # print(start_char, nbr[start_id+1]['weight'] if start_id + 1 in nbr else 0, out_weight)
            nbr = corpus.get_sorted_neighbour(start_char, end_char)
            text_json[i] = {"char": start_char, "outWeight": out_weight, "neighbour": nbr}
            i += 1
        json.dump(text_json, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        print("text json ready at: " + path)

    def draw(self):
        # nx.draw_networkx(self.text, font_family='SimHei', node_color='white')
        # nx.draw_spring(self.text, font_family='SimHei', node_color='white')
        nx.draw_shell(self.text, font_family='SimHei', node_color='black')
        plt.show()
