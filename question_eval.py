#!/usr/bin/etc python

import sys

evalFile = sys.argv[1]

ef = open(evalFile, 'r')
name = ""
name = raw_input("Enter your name: ")
annotations = open("qa_history/"+evalFile.replace(".txt","")+"_"+str(name)+"_annotated", 'w')
numQ = 0
oldScore = 0
newScore = 0
question = ""

for line in ef:
    #Diplay question
    if line[:2] == 'Q:':
        question = line[2:]
        numQ += 1
    if line[:3] == 'old':
        print "Q: " + question + "A: " + line[5:]
        s = input('Score from 1-5: ')
        oldScore += int(s)
        annotations.write(line+"\t"+"old"+"\t"+str(s)+"\n")
    if line[:3] == 'new':
        print "Q: " + question + "A: " + line[5:]
        s = input('Score from 1-5: ')
        newScore += int(s)
        annotations.write(line+"\t"+"new"+"\t"+str(s)+"\n")


ef.close()

os = oldScore / float(numQ)
ns = newScore / float(numQ)

print "Final evaluation:"
print "Average Old Score: " + str(os)
print "Average New Score: " + str(ns)

