import paho.mqtt.client as mqtt
import picamera
import pytz
from datetime import datetime

# Settings
path = "/home/pi/Surveillance-Camera/record/" # Record Folder
channel = "chattida/cctv" # MQTT Subscribe

state = False

def update_state():
    global state
    state = not state

def generate_filename():
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    now = now.strftime("%Y%m%d%H%M")
    return now

def on_connect(client, usedata, flags_dict, rc):
    if (rc == 0):
        print("Connected to MQTT Server")
        client.subscribe(channel)

def on_message(client, usedata, msg):
    # Convert msg to String (utf-8)
    msg = str(msg.payload, "utf-8")

    # if message equal 'trigger' -> update state
    if msg == "trigger":
        update_state()

    # if state equal True -> start record
    if state:
        filename = generate_filename()
        print("Start Recording")
        print("File: " + filename + ".h264")
        camera.start_recording(path + filename + ".h264")

    # if state equal False -> stop record
    if not state:
        print("Stop Recording")
        camera.stop_recording()

# Config picamera
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
camera.vflip = True

# Config MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Main
try:
    client.connect("broker.mqttdashboard.com", 1883)
    client.loop_forever()

except KeyboardInterrupt:
    client.disconnect()
    print("\nDisconected to MQTT Server")
