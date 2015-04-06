#!/usr/bin/etc python

import galbackend
#target = galbackend.GalInterface()
#print(target)
#gt = galbackend.Thread(target=galbackend.GalInterface)
galbackend.InitLogging()
galbackend.InitResource()
galbackend.LaunchQueryDebug("My name is Maya")
galbackend.get_response("when did you move to New York")


print ""