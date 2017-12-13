from wsgiref.simple_server import make_server
from Network import CorpusGraph
from Network import TextGraph
import json

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if method=='GET' and path=='/':
        body = '''<h6>enter your sentence</h6>
                <form action="/tokenization" method="post">
                <input name="sentence">
                <button type="submit">Parse</button> 
                  </form>'''
        return [body.encode('utf-8')]
    if method=="POST" and path=="/tokenization":
        with open("./presentation/WordLink.html","rb") as f:
            body=f.read()
        return [body]
    if method=='GET' and path=='/tokenize-result':
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
        res=json.dumps(tg.make_json(cg),ensure_ascii=False)
        return [res.encode('utf-8')]


httpd = make_server('',8000,application)
print("serving")
httpd.serve_forever()

