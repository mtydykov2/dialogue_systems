#!/usr/bin/etc python
import imp
import sys
sys.path.insert(1,"C:\\Users\\mtydykov\\actorimpersonator\\Agents")
sys.path.insert(1,"C:\\actorimpersonator\\Agents")

#galbackendold = imp.load_source('galbackend_old', "C:\\Users\\mtydykov\\actorimpersonator\\Agents\\Backend\\galbackend_old.py")
from Backend import galbackend as galbackendnew
from Backend_Old import galbackend_old as galbackendold
import random

import os

def record_responses(new, old, answer_key, responses, question):
    items = [(new, "new"), (old, "old")]
    random.shuffle(items)
    answer_key.write("\n\nQ:" + question + "\n")
    responses.write("\n\nQ:" + question + "\n")
    for i in items:
        answer_key.write(i[1] + ": " + i[0] + "\n")
        responses.write("A:" + i[0] + "\n")


f_name = "tick_tock_statements"
dir = "C:\\actorimpersonator\\Test_Questions\\"
f = open(dir+f_name+".txt")
answer_key = open(f_name+"_answer_key.txt","w")
responses = open(f_name+"_responses.txt","w")

question1 = ("My name is Maya")
galbackendold.InitLogging()
galbackendold.InitResource()
old = galbackendold.LaunchQueryDebug(question1)
galbackendnew.InitLogging()
galbackendnew.InitResource()
new = galbackendnew.LaunchQueryDebug(question1)
record_responses(new, old, answer_key, responses,question1)

for question in f:
    if question:
        new = galbackendnew.get_response(question)
        old = galbackendold.get_response(question)
        record_responses(new, old, answer_key, responses, question)
answer_key.close()
responses.close()