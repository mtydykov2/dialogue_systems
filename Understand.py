#!/usr/bin/etc python

import nltk

from collections import defaultdict
import NEDialogueTagger

def AddWeight(tag_list, rules, stop_dict, question_words, ne_list):
    result = []
    sent = " ".join(tok[0] for tok in tag_list)
    added_nes = []
    tok_to_ne = {}
    # populate data structure which keeps track of start & end indices of NEs in a sentence, since they may span multiple tokens
    for k in ne_list.keys():
        for ne in ne_list[k]:
            tok_to_ne[sent.index(ne)]=sent.index(ne)+len(ne),k
    for i, (token, pos) in enumerate(tag_list):
        ne = "O"
        added_rule = False
        start_index = sent.index(token)
        # if this token is a starting token of a NE
        if start_index in tok_to_ne.keys():
            end_index = tok_to_ne[start_index][0]
            ne = tok_to_ne[start_index][1]
            # if we have not yet added this NE
            if (start_index, end_index) not in added_nes:
                # the weight should be 5 and it should appear in the answer. use the POS of the first token in NE.
                result += [(sent[start_index:end_index], pos, 5, ne)]
                added_nes.append((start_index, end_index,))
                added_rule = True
        # make sure this token wasn't already added to matching rules as part of NE
        for start, end in added_nes:
            if start_index > start and start_index < end:
                added_rule = True
        # if we haven't added a rule for this token yet
        if not added_rule:
            # add a rule to match this token's POS, if POS is in rules dict. can match answer or question
            if rules[pos]>0:
                result += [(token, pos, rules[pos], ne)]
            else:
                #ignore periods
                if pos==".":
                    continue
                # ignore stopwords. all other words (not in rule dict) get a weight of 1 and can match answer or question
                if not stop_dict[token] :
                    result += [(token.lower(), pos, 1, ne)]
                # do not ignore question words (who, where, when). they get a weight of 1 and can match answer or question.
                if token in question_words:
                    result += [(token.lower(), pos, 1, ne)]
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


