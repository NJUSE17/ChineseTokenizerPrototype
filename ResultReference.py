import jieba
import re


def compare(pivot_array, testing_array):
    character_offset = 0
    pivot_word_offsets = set()
    for word in pivot_array:
        pivot_word_offsets.add((character_offset, len(word)))
        character_offset += len(word)

    testing_word_offsets = set()
    character_offset = 0
    for word in testing_array:
        testing_word_offsets.add((character_offset, len(word)))
        character_offset += len(word)

    return 1 if len(pivot_word_offsets) == 0 else len(pivot_word_offsets & testing_word_offsets) / (
        len(pivot_word_offsets) + 0.0)


class JiebaChecker:
    def __init__(self):
        self.ptn = re.compile("[\u4e00-\u9fa5]+$")

    def check(self, init_sentence, token_result):
        print("original sentence: %s" % init_sentence)
        print("token_result"+str(token_result))
        if init_sentence.strip() == "":
            return None

        jieba_result_gen = jieba.cut(init_sentence)
        jieba_result = []
        for jieba_word in jieba_result_gen:
            if self.is_chinese(jieba_word):
                jieba_result.append(jieba_word)
        compare_jieba_graphx = compare(jieba_result, token_result)
        return {"overlap": compare_jieba_graphx, "jieba_result": jieba_result}

    def is_chinese(self, word):
        if re.match(self.ptn, word) is not None:
            return True
        else:
            return False

