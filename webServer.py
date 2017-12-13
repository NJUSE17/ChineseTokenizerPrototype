import os
from wsgiref.simple_server import make_server
from Network import CorpusGraph
from Network import TextGraph
import json


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if method == 'GET' and path == '/':
        body = '''<h6>enter your sentence</h6>
                <form action="/tokenization" method="post">
                <input name="sentence">
                <button type="submit">Parse</button> 
                  </form>'''
        return [body.encode('utf-8')]
    if method == "POST" and path == "/tokenization":
        with open("./presentation/WordLink.html", "rb") as f:
            body = f.read()
        return [body]
    if method == 'GET' and path == '/tokenize-result':
        cg = CorpusGraph()
        cg.load_from_json()
        # cg.build_corpus()
        # cg.save_as_json()
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
        res = json.dumps(tg.make_json(cg), ensure_ascii=False)
        return [res.encode('utf-8')]


def content_type(path):
    if path.endswith(".css"):
        return "text/css"
    elif path.endswith(".js"):
        return "*/*"
    elif path.endswith(".html"):
        return "text/html"
    else:
        return "*/*"


def app(environ, start_response):
    path_info = environ["PATH_INFO"]
    resource = "WordLink.html"
    if '/' in path_info:
        subroot = path_info.split("/")[1]
        resource = subroot if subroot != "" else resource

    headers = [("Content-Type", content_type(resource))]

    resp_file = os.path.join("./presentation", resource)

    print("######### 读取文件 %s ##########" % resp_file)
    try:
        with open(resp_file, "rb") as f:
            resp_file = f.read()
    except Exception:
        start_response("404 Not Found", headers)
        return ["404 Not Found"]

    start_response("200 OK", headers)
    return [resp_file]


httpd = make_server('localhost', 8000, app)
print("serving")
httpd.serve_forever()
