import paho.mqtt.client as mqtt
import picamera
import pytz
import RPi.GPIO as GPIO
from datetime import datetime
import subprocess
import os

# Settings
path = "/home/pi/Surveillance-Camera/record/" # Record Folder
channel = "chattida/cctv" # MQTT Subscribe

GPIO.setmode(GPIO.BCM)
LIGHT = 4

GPIO.setwarnings(False)
GPIO.setup(LIGHT,GPIO.OUT)

state = False

def update_state():
    global state
    state = not state

def generate_filename():
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    now = now.strftime("%Y%m%d%H%M%S")
    return now

def on_connect(client, usedata, flags_dict, rc):
    if (rc == 0):
        print("Connected to MQTT Server")
        client.subscribe(channel)

def on_message(client, usedata, msg):
    # Convert msg to String (utf-8)
    msg = str(msg.payload, "utf-8")

    # if message equal 'trigger' -> update state
    if msg.lower() == "trigger":
        update_state()
        
        # if state equal True -> start record
        if state:
            filename = generate_filename()
            print("Start Recording")
            print("File: " + filename + ".h264")
            # check folder is exist if not create
            if not os.path.exists(path):
                os.makedirs(path)
            # start recording
            camera.start_recording(path + filename + ".h264")
            # turn on light
            GPIO.output(LIGHT,True)

        # if state equal False -> stop record
        if not state:
            print("Stop Recording")
            # stop recording
            camera.stop_recording()
            # turn off light
            GPIO.output(LIGHT,False)
            # sync folder
            sync = subprocess.Popen(['python3', 'sync.py'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)

# Config picamera
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
camera.vflip = True

# Config MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Clear Light
GPIO.output(LIGHT,False)

# Main
try:
    client.connect("broker.mqttdashboard.com", 1883)
    client.loop_forever()

except KeyboardInterrupt:
    client.disconnect()
    print("\nDisconected to MQTT Server")
