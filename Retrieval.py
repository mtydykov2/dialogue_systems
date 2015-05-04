#!/usr/bin/env python

"""
find answer in database and by search engine
"""
import random
from collections import defaultdict


#penalize too long sentence/ low relavance
def Select(Candidates):
    threshold = 15
    answer_list = []
    answer_strings = []

    print "Candidates for select ", Candidates

    fileout = open('60question.txt', 'a') ## only for the use of retrieval_question
    for i in range(0, min(3, len(Candidates))):
        fileout.write(' '.join(Candidates[i][1]))
        fileout.write(' '.join(Candidates[i][2])+'\n')
    fileout.write('\n')
    fileout.close

    for score, question, question_pos_tags, question_ne_tags, answer, answer_pos_tags, answer_ne_tags, tag in Candidates:
        if len(answer) > threshold:
            continue
        #MT: Added to replace random names with the person's name
        astring = " ".join(answer)
        if "PERSON" in answer_ne_tags.keys():
            f = open("person_name")
            person_name = f.readline()
            names = answer_ne_tags["PERSON"]
            for name in names:
                astring = astring.replace(name, person_name)
            answer = astring.split()

        astring = " ".join(answer)
        if astring.find('--')!=-1 or astring.find(':')!=-1:
            continue
        if astring in answer_strings:
            continue

        answer_strings.append(astring)

        answer_list += [(score, answer, tag)]
    if len(answer_list) > 0:
        result = random.choice(answer_list)
        return result
        #return answer_list[0]
    else:
        return (0, [], '')

def FreqPairMatch(info, database, select=5):
    Candidate = []
    Candidate = get_score_updates(database, "Q", info, Candidate, 1, select)
    Candidate = get_score_updates(database,"A", info, Candidate, 1, select)

    if len(Candidate)>0:
        topiclevel = 1
    else:
        topiclevel = -1

    return Candidate, topiclevel

def scoreNes(database, utterance_type, info, candidates, score_coefficient, select, user_query_dict):
    nes_to_match = []
    for user_tok in user_query_dict.keys():
        if user_tok == "where":
            nes_to_match.append("LOCATION")
        if user_tok == "who":
            nes_to_match.append("PERSON")
        if user_tok == "when":
            nes_to_match.append("DATE")
    return nes_to_match


def get_score_updates(database, utterance_type, info, candidates, score_coefficient, select):
    user_query_dict = {tup[0]:[tup[1],tup[2],tup[3],tup[4]] for tup in info}
    nes_to_match = []
    if utterance_type == "A":
        nes_to_match = scoreNes(database, utterance_type, info, candidates, score_coefficient, select, user_query_dict)
    for idx, utter_allcases in database[utterance_type].items():
        utter = [word.lower() for word in utter_allcases]
        # only look at things with short-ish answers
        if len(database["A"][idx]) < 15:
            score = 0
            # treat named entities separately, since they should really match in groups
            for ne in database[utterance_type+"_ne_tagged"][idx]:
                # if we find a general NE type that we're looking for, increase score
                if ne in nes_to_match:
                    score += 5
            # don't want to double-match the same rule on both POS and NE. only try here if the NE did not match
            for i, token in enumerate(user_query_dict.keys()):
                # if it's a named entity, just check for matching words here (as long as it's the right utterance type)
                if user_query_dict[token][2] != "O":
                    if token in " ".join(utter) and (user_query_dict[token][-1]=="BOTH" or user_query_dict[token][-1]==utterance_type):
                        score += user_query_dict[token][1]
                # otherwise, check for POS
                elif token in utter:
                        # get the within-list token index from database
                        list_index = utter.index(token)
                        if (database[utterance_type+"_pos_tags"][idx][list_index] == user_query_dict[token][0]) and (user_query_dict[token][-1]=="BOTH" or user_query_dict[token][-1]==utterance_type):
                            score += user_query_dict[token][1]
            score = score_coefficient*float(score)/(len(info)+len(utter))
            if score > 0:
                candidates = UpdateCandidatePair(idx, database, score, candidates, select, utterance_type)
    return candidates

def UpdateCandidatePair(idx, database, score, Candidate, select, tag):
        add = False
        if len(Candidate) < select:
                Candidate += [(score, database['Q'][idx], database['Q_pos_tags'][idx], database['Q_ne_tagged'][idx], database['A'][idx],database['A_pos_tags'][idx],database['A_ne_tagged'][idx], tag)]
                add = True
        else:
                if score > Candidate[select-1][0]:
                        Candidate[select-1] = (score, database['Q'][idx], database['Q_pos_tags'][idx], database['Q_ne_tagged'][idx], database['A'][idx],database['A_pos_tags'][idx],database['A_ne_tagged'][idx], tag)
                        add = True
        if add:
                return sorted(Candidate, key=lambda item:item[0], reverse=True)
        else:
                return Candidate

