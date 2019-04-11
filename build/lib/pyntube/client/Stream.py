import threading
import requests
import json
import cv2
import numpy
from win32api import GetSystemMetrics
class Stream():
    def run(self):
        self.activeThreads = []
        self._control_thread = threading.Thread(target=self.control_thread)
        self._video_thread = threading.Thread(target=self.video_thread)
        self._audio_thread =threading.Thread(target=self.audio_thread)

        self._control_thread.start()
    def control_thread(self):
        r = requests.post(self.serverURL+"/api/stream")
        if r.status_code == 200:
            self.streamID = json.loads(r.text)["streamID"]
            self.streamKey = json.loads(r.text)["streamKey"] 
            print(f"Stream starting! Watch on {self.serverURL}/watch/{self.streamID}")

            self._video_thread.start()
            self._audio_thread.start()
        else:
            print("Stream creation denied")
            print(r.text)
    def video_thread(self):
        while True:
            monitor = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
    def audio_thread(self):
        pass
    def onError(self,error):
        raise error
    def __init__(self,serverURL):
        self.serverURL = serverURL