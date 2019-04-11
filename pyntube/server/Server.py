import flask
from . import utils
import json
import base64
import time

server = flask.Flask(__name__)
context = {
    "streams":{},
    "streamdata":{}
}

#Streaming api
@server.route("/api/stream",methods=["POST"])
def createStream():
    streamID = utils.newStreamID(context)
    streamKey = utils.newStreamKey(context, streamID)
    context["streams"][streamID] = streamKey
    context["streamdata"][streamID] = {"video":None,"audio":None}
    return json.dumps({
        "streamID":streamID,
        "streamKey":streamKey
    })


#Video api
def GetVideoFeed(user):
    while True:
        try:
            val = utils.getImgFeed(context,user)
            time.sleep(.1)
        except Exception as e:
            raise(e)
            #val = base64.decodebytes(b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
        yield (b'--frame\r\n' +b'Content-Type: image/jpeg\r\n\r\n' + val + b'\r\n')
@server.route("/api/video_feed/<string:user>")
def SendVideoFeed(user):
    return flask.Response(GetVideoFeed(user), mimetype='multipart/x-mixed-replace; boundary=frame')
@server.route("/api/stream/<string:user>/video",methods=["put"])
def addVideoFeed(user):
    global context
    try:
        if context["streams"][user] == flask.request.headers["key"]:
            context = utils.setImgFeed(context,user,flask.request.files["img"])
            return "Processing..."
        else:
            return "Invalid auth"
    except Exception as e:
        raise(e)
        #return "Server issue"

#Audio feed
def GetAudioFeed(user):
    global context
    sendHeader = True
    c = 0
    while True:
        if c == 100:return
        c += 1
        if sendHeader:
            chunk = utils.genHeader(44100,16,1,50000)
            sendHeader = False
            yield chunk
        else:
            chunk = context["streamdata"][user]["audio"]
            yield chunk
        time.sleep(0.1)

@server.route("/api/audio_feed/<string:user>")
def SendAudioFeed(user):
    return flask.Response(flask.stream_with_context(GetAudioFeed(user)))

@server.route("/api/stream/<string:user>/audio",methods=["PUT"])
def AddAudioFeed(user):
    global context
    try:
        if context["streams"][user] == flask.request.headers["key"]:
            context["streamdata"][user]["audio"] = flask.request.data
            return "Processing..."
        else:
            return "Invalid auth"
    except Exception as e:
        raise(e)
        #return "Server issue"
#GUI
@server.route("/watch/<string:user>")
def watchGui(user):
    return f'''<html><body><img src="/api/video_feed/{user}"></html></body>     <audio controls>
        <source src="/api/audio_feed/{user}" type="audio/x-wav;codec=pcm">
        Your browser does not support the audio element.
        </audio>'''