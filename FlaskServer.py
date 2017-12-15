from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import send_file
from Network import CorpusGraph
from Network import TextGraph
from ResultReference import JiebaChecker
import os
import json

cg = CorpusGraph()
cg.load_from_json()
checker = JiebaChecker()
app = Flask(__name__, template_folder='./presentation', static_folder='./presentation')


@app.route('/')
def hello_world():
    return send_file('./presentation/WordLink.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'presentation'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<loadfile>', methods=['POST', 'GET'])
def load_ref(loadfile):
    print(loadfile)
    return send_from_directory(os.path.join(app.root_path, 'presentation'), loadfile)


@app.route('/tokenize-result', methods=['GET', 'POST'])
def tokenize():
    if request.method == 'GET':
        tg = TextGraph()
        # sentences = tg.get_sentences(isRandom=False)
        sentence = "没有输入"

        if request.args.get('sentence', '') != "":
            sentence = request.args.get('sentence', '')
        tg.build([sentence])
        tg.fill_edge(cg)

        # 暂时只对单句分词
        result = tg.cut()[0]
        check = checker.check(sentence, result)

        jieba_result = check["jieba_result"]
        overlap = check["overlap"]
        res = json.dumps(
            {"graph": tg.make_json(cg, path=None), "result": result, "jieba": jieba_result, "overlap": overlap},
            ensure_ascii=False)
        return res


if __name__ == '__main__':
    app.run(host="localhost", port="8000")
