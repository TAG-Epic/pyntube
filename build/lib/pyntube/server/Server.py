import flask
from . import utils
import json
import base64

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
    return json.dumps({
        "streamID":streamID,
        "streamKey":streamKey
    })


#Video api
def GetVideoFeed(user):
    global context
    while True:
        try:
            val, context = utils.getImgFeed(context,user)
        except:
            val = base64.decodebytes(b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")

        yield val
@server.route("/api/video_feed/<str:user>")
def SendVideoFeed(user):
    return flask.Response(GetVideoFeed(user), mimetype='multipart/x-mixed-replace; boundary=frame')
@server.route("/api/stream/<str:user>/video")
def addVideoFeed(user):
    try:
        if context["streams"][flask.request.headers["id"]] == flask.request.headers["key"]:
            context = utils.setImgFeed(context,user,flask.request.files["img"])
            return "Processing..."
        else:
            return "Invalid auth"
    except:
        return "Invalid auth"