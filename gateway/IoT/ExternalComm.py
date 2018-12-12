import os
import paho.mqtt.client as mqttc
import paho.mqtt.publish as publish
import Home
import subprocess

MQTT_REMOTE_SERVER = "localhost"
# MQTT_REMOTE_SERVER = "192.168.43.103"
MQTT_PATH_SEND = "home_1_0"
MQTT_PATH_RECV = "home_1_1"
USR = "danny"
PASS = "danny"


class ExternalComm:
    def __init__(self, home):
        print("new ExternalComm created")
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(USR, PASS)
        self.client.connect(MQTT_REMOTE_SERVER, 1883, 60)
        assert isinstance(home, Home.Home)
        self.myHome = home
        print("connected")

    @staticmethod
    def send_tmp(tmp):
        try:
            publish.single(MQTT_PATH_SEND, "tmp:" + tmp, hostname=MQTT_REMOTE_SERVER,
                           auth={'username': USR, 'password': PASS})
        except Exception as ex:
            print("Error in send_tmp(). ex: {}".format(ex))
        # TODO: store tmp value and send it later

    @staticmethod
    def send_alarm():
        try:
            publish.single(MQTT_PATH_SEND, "alarm", hostname=MQTT_REMOTE_SERVER,
                           auth={'username': USR, 'password': PASS})
        except Exception as ex:
            print("Error in send_alarm(). ex: {}".format(ex))

    @staticmethod
    def send_status(st):
        try:
            publish.single(MQTT_PATH_SEND, "status:" + st, hostname=MQTT_REMOTE_SERVER,
                           auth={'username': USR, 'password': PASS})
        except Exception as ex:
            print("Error in send_status(). ex: {}".format(ex))

    @staticmethod
    def send_light(st):
        try:
            publish.single(MQTT_PATH_SEND, "light:" + st, hostname=MQTT_REMOTE_SERVER,
                           auth={'username': USR, 'password': PASS})
        except Exception as ex:
            print("Error in send_status(). ex: {}".format(ex))

    def toggle_light(self):
        self.myHome.toggle_light()

    def start(self):
        print("looping ...")
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        print("ExternalComm: got a message")
        print("%s %s" % (msg.topic, msg.payload))
        info = msg.payload.decode("ascii")
        if info == "start_streaming":
            print("starting streaming...")
            # os.system('python3 streaming.py')
            self.process = subprocess.Popen(['python3', 'streaming.py'])
        elif info == "stop_streaming":
            print("stop streaming...")
            self.process.kill()
        elif info == "light":
            print("ext: must toggle light")
            self.myHome.toggle_light()

    def on_connect(self, client, userdata, flags, rc):
        print("External Comm: connected with result code " + str(rc))
        client.subscribe(MQTT_PATH_RECV)

