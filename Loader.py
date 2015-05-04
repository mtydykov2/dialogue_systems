#!/usr/bin/etc python

import nltk
from collections import defaultdict
import json
import os.path as path
import os
question_words = ["who","what","where","why", "when"]

def LoadLanguageResource():
        WeightRules=defaultdict(int)
        nounlist = ['NN', 'NNS', 'NNP', 'NNPS']
        for noun in nounlist:
                WeightRules[noun] = 3
        WeightRules['VBP'] = 1
        stop_dict=defaultdict(bool)
        for word in nltk.corpus.stopwords.words('english'):
                stop_dict[word] = True
        resource = {}
        resource['rules'] = WeightRules
        resource['stop_words'] = stop_dict
        resource['question_words'] = question_words
        return resource

def LoadData(datalist):
	database = {}
	for datafile in datalist:
		f = open(datafile)
		line = f.readline()
		f.close()
		raw_data = json.loads(str(line.strip()))
		database = PushData(raw_data, database)
	return database

def PushData(data, database):
	last = len(database.keys())
	for pair in data:
		database[last] = pair['question_tokens']
		last += 1
		database[last] = pair['answer_tokens']
		last += 1
	return database

def LoadDataPair(datalist):
        database = {}
        database['Q'] = {}
        database['A'] = {}
        database['Q_pos_tags'] = {}
        database['A_pos_tags'] = {}
        database['Q_ne_tagged'] = {}
        database['A_ne_tagged'] = {}

        for datafile in datalist:
                f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)),datafile))
                line = f.readline()
                f.close()
                raw_data = json.loads(str(line.strip()))
                database = PushDataPair(raw_data, database)
        return database

#modified to include POS/NE tags for all questions and answers
def PushDataPair(data, database):
        last = len(database['Q'].keys())
        for pair in data:
                database['Q'][last] = pair['question_tokens']
                database['A'][last] = pair['answer_tokens']
                database['Q_pos_tags'][last] = pair['question_pos_tagged']
                database['A_pos_tags'][last] = pair['answer_pos_tagged']
                database['Q_ne_tagged'][last] = pair['question_ne_tagged']
                database['A_ne_tagged'][last] = pair['answer_ne_tagged']
                last += 1
        return database

def LoadTemplate(filelist):
	Library = {}
	for filepath in filelist:
		name = path.splitext(path.basename(filepath))[0]	
		Library[name] = [line.strip() for line in open(os.path.join(os.path.abspath(os.path.dirname(__file__)),filepath))]
	return Library

def LoadTopic(topicfile):
	return [line.strip() for line in open(topicfile)]

