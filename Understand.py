#!/usr/bin/etc python

import nltk

from collections import defaultdict
import NEDialogueTagger

def AddWeight(tag_list, rules, stop_dict, question_words, ne_list):
    result = []
    sent = " ".join(tok[0] for tok in tag_list)
    added_nes = []
    tok_to_ne = {}
    for k in ne_list.keys():
        for ne in ne_list[k]:
            tok_to_ne[sent.index(ne)]=sent.index(ne)+len(ne),k
    for i, (token, pos) in enumerate(tag_list):
        ne = "O"
        added_rule = False
        start_index = sent.index(token)
        if start_index in tok_to_ne.keys():
            end_index = tok_to_ne[start_index][0]
            ne = tok_to_ne[start_index][1]
            if start_index not in added_nes:
                result += [(sent[start_index:end_index], pos, 5, ne, "A")]
                added_nes.append(start_index)
                added_rule = True
        if not added_rule:
            if rules[pos]>0:
                result += [(token, pos, rules[pos], ne, "BOTH")]
            else:
                if pos==".":
                    continue
                if not stop_dict[token] :
                    result += [(token.lower(), pos, 1, ne, "BOTH")]
                if token in question_words:
                    result += [(token.lower(), pos, 1, ne, "BOTH")]

    return result

#return [(token, pos_tag, weight)]
def InfoExtractor(utter, resource):
    rules = resource['rules']
    stop_dict = resource['stop_words']
    question_words = resource['question_words']
    tokens = nltk.word_tokenize(utter)
    tag_list = nltk.pos_tag(tokens)
    ne_list = NEDialogueTagger.ner_tag_tokens(tokens)
    return AddWeight(tag_list, rules, stop_dict, question_words, ne_list)


