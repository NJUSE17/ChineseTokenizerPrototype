import os
from wsgiref.simple_server import make_server
from Network import CorpusGraph
from Network import TextGraph
import json



cg = CorpusGraph()
cg.load_from_json()
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
    method = environ['REQUEST_METHOD']
    if method == 'GET' and path_info == '/tokenize-result':
        tg = TextGraph()
        # sentences = tg.get_sentences(isRandom=False)
        sentences = ["准许原告肖振明撤回起诉"]
        tg.build(sentences)
        tg.fill_edge(cg)
        res = json.dumps(tg.make_json(cg), ensure_ascii=False)
        return [res.encode('utf-8')]

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
