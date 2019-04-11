import os
import random
import string

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
    val = context["streamdata"][user]["video"]
    return val
def setImgFeed(context,user,img):  
    context["streamdata"][user]["video"] = img.read()
    return context

def genHeader(sampleRate, bitsPerSample, channels, samples):
    datasize = samples * channels * bitsPerSample // 8
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o
