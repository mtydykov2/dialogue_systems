__author__ = 'Maya Tydykov'
import nltk
import os
import Loader
import json
import sys

from nltk.tag.stanford import NERTagger
model = os.path.join(os.path.dirname(__file__), 'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz')
jar = os.path.join(os.path.dirname(__file__), 'stanford-ner/stanford-ner.jar')
st = NERTagger(model, jar)
os.environ['JAVAHOME'] = os.getenv('JAVA_HOME')+"/bin/"
listfiles=['cnn_qa.list','movies.list']

def ner_tag_tokens(token_list):
    result = st.tag(token_list)[0]
    ret = {}
    i = 0
    while i < len(result):
        added = False
        if i < len(result) and result[i][1] != "O":
            begin = i
            added = True
            i+=1
            while i < len(result) and result[i][1] == result[i-1][1] and result[i][1] != "O":
                i+=1
        if added:
            if result[i-1][1] not in ret.keys():
                string = " ".join([word[0] for word in result[begin:i]])
                ret[result[i-1][1]] = [string]
            else:
                ret[result[i-1][1]].append(" ".join(word[0] for word in result[begin:i]))

        if not added: i += 1
    return ret

def preprocess_database():
    datalist=[line.strip() for listfile in listfiles for line in open(listfile)]
    datalist_new = []
    for datafile in datalist:
        f = open(datafile)
        line = f.readline()
        f.close()
        raw_data = json.loads(str(line.strip()))
        for el in raw_data:
            tokens_answer =  nltk.word_tokenize(el['answer'])
            tokens_question = nltk.word_tokenize(el['question'])
            tags_answer = st.tag(tokens_answer)
            tags_question = st.tag(tokens_question)
            ne_tags_question = []
            ne_tags_answer = []
            pos_tags_answer = [token[1] for token in nltk.pos_tag(tokens_answer)]
            pos_tags_question = [token[1] for token in nltk.pos_tag(tokens_question)]
            for tag_answer in tags_answer:
                if tag_answer[1] != "O":
                    ne_tags_answer.append(tags_answer.index(tag_answer))

            for tag_question in tags_question:
                if tag_question[1] != "O":
                    ne_tags_question.append(tags_question.index(tag_question))

            el['answer_ne_tags'] = ne_tags_answer
            el['question_ne_tags'] = ne_tags_question
            el['answer_pos_tags'] = pos_tags_answer
            el['question_pos_tags'] = pos_tags_question
        with open("alldata-json/"+f.name[(f.name.rindex("/")+1):]+"_ne_tagged", "w") as outfile:
            s = json.dumps([dict for dict in raw_data])
            outfile.write(s)
        datalist_new.append(f.name[(f.name.rindex("/")+1):]+"_ne_tagged")
    f = open("movies.list","w")
    for fname in datalist_new:
        f.write("alldata-json/"+fname+"\n")

if __name__ == "__main__":
    #preprocess_database()
    tokens = nltk.word_tokenize("My name is Angelina Jolie, his name is Brad Pitt, and they live in London.")
    print ner_tag_tokens(tokens)