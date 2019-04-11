import os
import random
import string
import datetime

def randomString(length):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])
def newStreamID(context):
    while True:
        uid = randomString(10)
        if not uid in context["streams"].keys():
            return uid
def newStreamKey(context, streamID):


    usedID = False
    segmentsUsed = 0
    key = ""

    splittedID = list(streamID)
    idsegment = "".join(splittedID[2:9])
    randomSegments = [randomString(8) for i in range(9000)]

    while segmentsUsed != 100:
        if random.choice([True,False,False,False,False,False,False,False,False,False]) == True:
            if not usedID:
                usedID = True
                key += idsegment
        else:
            key += random.choice(randomSegments)
            segmentsUsed += 1
    return key
def getImgFeed(context,user):
    timestamp = datetime.datetime.now()
    val = context.pop(context["streamdata"][user]["video"][timestamp])
    return val, context
def setImgFeed(context,user,img):
    timestamp = datetime.datetime.now()- datetime.time(seconds=10)
    context["streamdata"][user]["video"][timestamp] = img
    return context

