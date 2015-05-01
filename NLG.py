#!/usr/bin/env python

import random
import os
def GenerateResponsePair(TopicLevel, Candidates, refine_strategy=-1):
        if TopicLevel==-1: #off topic
                output = 'Ok. Tell me more about yourself.'
        else:
		select = random.choice(Candidates)
		pair = [select[1], select[2]]
                output = [" ".join(pair[0]), " ".join(pair[1])]

        return output

def FillTemplate(TemplateLib, TopicLib, template, answer=[]):
    answerString = ' '.join(answer)
    topic_number = len(TopicLib)
    sent_list = []
    for item in template:
        for unit in item.split(','):
            if unit == 'answer':
                sent_list.append(answerString)
            elif unit == 'topic':
                topic_history = [line.strip() for line in open(os.path.join(os.path.dirname(__file__),'topic_history.txt'))]
                fileout = open('topic_history.txt', 'a')
                while unit == 'topic':
                    #bug fix: randint INCLUDES the upper bound, so must decrement by 1 to avoid
                    #going out of index
                    topic_id = random.randint(1, topic_number-1)
                    if int(topic_history[-1]) != topic_id:
                        break
                fileout.write(str(topic_id)+'\n')
                sent_list.append(TopicLib[topic_id])
            else:
                sent_list.append(random.choice(TemplateLib[unit]))
    print "template answer ", sent_list
    return ' '.join(sent_list)