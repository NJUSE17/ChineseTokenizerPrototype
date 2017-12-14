from flask import Flask
from flask import request
from flask import render_template
from Network import CorpusGraph
from Network import TextGraph
import json


cg = CorpusGraph()
cg.load_from_json()
app=Flask(__name__,template_folder='./presentation')

@app.route('/')
def hello_world():
    return render_template('WordLink.html')
@app.route('/<loadfile>',methods=['POST','GET'])
def loadRef(loadfile):
    return render_template(loadfile)

@app.route('/tokenize-result',methods=['GET','POST'])
def tokenize():
   if request.method=='GET':
       tg = TextGraph();
       sentences =request.args.get('sentence','')
       tg.build(sentences)
       tg.fill_edge(cg)
       res = json.dumps(tg.make_json(cg, path=None), ensure_ascii=False)
       print(res)
       return res


if __name__=='__main__':
    app.run(host="localhost",port="8000")