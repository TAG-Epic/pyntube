import threading
import requests
import json
import cv2
import numpy
import mss
from PIL import Image
import pyaudio
import os
import time

class Stream():
    def run(self):
        self._control_thread = threading.Thread(target=self.control_thread)
        self._video_thread = threading.Thread(target=self.video_thread)
        self._audio_thread = threading.Thread(target=self.audio_thread)
        self.audio_rate = 0.0
        self.video_rate = 0.0

        self._control_thread.start()
    def control_thread(self):
        r = requests.post(self.serverURL+"/api/stream")
        if r.status_code == 200:
            self.streamID = json.loads(r.text)["streamID"]
            self.streamKey = json.loads(r.text)["streamKey"] 
            print(f"Stream starting! Watch on {self.serverURL}/watch/{self.streamID}")

            self._video_thread.start()
            self._audio_thread.start()


            while True:
                os.system(f"title FPS: {self.video_rate} AR: {self.audio_rate}")

        else:
            print("Stream creation denied")
            print(r.text)
    def video_thread(self):
        with mss.mss() as sc:
            while True:
                start_time = time.time()
                raw_img = sc.grab({"top": 40, "left": 0, "width": 800, "height": 640})
                img = Image.frombytes("RGB", raw_img.size, raw_img.bgra, "raw", "BGRX")
                img.save("shot.f","jpeg",quality=100)
                h = {
                    "key":self.streamKey
                }
                f = {
                    "img":open("shot.f","rb")
                }
                r = requests.put(self.serverURL+f"/api/stream/{self.streamID}/video", headers=h,files=f)
                self.video_rate = 1.0 / (time.time() - start_time)
    def audio_thread(self):
        audio = pyaudio.PyAudio()
        self.audio_stream = audio.open(format=self.audioSettings["FORMAT"], channels=self.audioSettings["CHANNELS"],rate=self.audioSettings["RATE"], input=self.audioSettings["INPUT"],frames_per_buffer=self.audioSettings["FRAMES_PER_BUFFER"])
        # Current chunk of audio data
        h = {
            "key":self.streamKey
        }
        while True:
            start_time = time.time()
            data = self.audio_stream.read(self.audioSettings["FRAMES_PER_BUFFER"])
            requests.put(self.serverURL+f"/api/stream/{self.streamID}/audio",headers=h,data=data)
            self.audio_rate = 1.0 / (time.time() - start_time)
    def onError(self,error):
        raise error
    def setAudioSettings(self,FORMAT=None,CHANNELS=None,RATE=None,INPUT=None,FRAMES_PER_BUFFER=None):
        if FORMAT != None:
            self.audioSettings["FORMAT"] = FORMAT
        if CHANNELS != None:
            self.audioSettings["CHANNELS"] = CHANNELS
        if RATE != None:
            self.audioSettings["RATE"] = RATE
        if INPUT != None:
            self.audioSettings["INPUT"] = INPUT
        if FRAMES_PER_BUFFER != None:
            self.audioSettings["FRAMES_PER_BUFFER"] = FRAMES_PER_BUFFER
    def __init__(self,serverURL):
        self.serverURL = serverURL
        self.audioSettings = {"FORMAT":pyaudio.paInt16,"CHANNELS":1,"RATE":44100,"INPUT":True, "FRAMES_PER_BUFFER":1024}