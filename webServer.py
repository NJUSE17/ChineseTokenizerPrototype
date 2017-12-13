import os
import re
from wsgiref.simple_server import make_server
from Network import CorpusGraph
from Network import TextGraph
import json
# from cgi import parse_qs, escape
from urllib.parse import parse_qs



cg = CorpusGraph()
cg.load_from_json()
def content_type(path):
    if path.endswith(".css"):
        return "text/css"
    elif path.endswith(".js"):
        return "*/*"
    elif path.endswith(".html"):
        return "text/html"
    elif path.endswith(".json"):
        return "*/*"
    else:
        return None


def app(environ, start_response):
    path_info = environ["PATH_INFO"]
    method = environ['REQUEST_METHOD']

    if method == 'GET' and '/tokenize-result' in path_info:
        tg = TextGraph()
        # sentences = tg.get_sentences(isRandom=False)
        sentences = ["没有输入"]

        query = environ['QUERY_STRING']
        parsed_query = parse_qs(str(query))
        sentences = parsed_query["sentence"]
        tg.build(sentences)
        tg.fill_edge(cg)
        res = json.dumps(tg.make_json(cg,path=None), ensure_ascii=False)
        print(res)
        start_response("200 OK", [("Content-Type", "application/json")])
        return [res.encode('utf-8')]

    resource = "WordLink.html"
    if '/' in path_info:
        subroot = path_info.split("/")[1]
        resource = subroot if subroot != "" else resource

    ctype = content_type(resource)
    if ctype is None:
        start_response("404 Not Found", [("Content-Type", "*/*")])
        return ["404 Not Found"]

    headers = [("Content-Type", ctype)]
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
