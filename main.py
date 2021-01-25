import paho.mqtt.client as mqtt
import json
import time
import ssl
import os
import datetime
import collections
import requests


# MQTT Configuration from Docker-Envs
username = os.environ['MQTT_USER']
password = os.environ['MQTT_PASSWORD']
host = os.environ['MQTT_HOST']
port = os.environ['MQTT_PORT', 8883]
tls = os.environ['TLS_BOOL', True]
sub_topic = os.environ['SUB_TOPIC']
debug = os.environ['DEBUG', False]
iota_endpoint = os.environ['IOTA_ENDPOINT']
api_key = os.environ['API_KEY']

class GlendimplexAdapter:

    def __init__(self, username, password, host, port, tls, sub_topic, debug, iota_endpoint, api_key):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.tls = tls
        self.sub_topic = sub_topic
        self.debug = debug
        self.iota_endpoint = iota_endpoint
        self.api_key = api_key

        self.client = mqtt.Client()
        self.timestamp = None
        self.payload = None
        self.device = None

    def send_http(self):
        try:
            query_parameters = {"i": self.device, "t": self.timestamp, "k": self.api_key}      # i = fiware device ID, t = timestamp, k = API Key
            r = requests.post(self.iota_endpoint, data = self.payload, params = query_parameters)
            if self.debug == True:
                print(datetime.datetime.now(), "- (HTTP) Sent Values to IoT-Agent with Status: ", r.status_code)
                print("Query Parameters: ", query_parameters)
        except Exception as e:
            print(datetime.datetime.now(), "- (HTTP) Could not send Request with Error: ", e)

    def on_connect(self, rc):

        if rc == 0:
            print(datetime.datetime.now(), "- (MQTT) connected")

        else:
            print(datetime.datetime.now(), "- (MQTT) Connection Error: ", rc)

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload)
        
        self.payload = {}
        try:
            topic = msg.topic
            self.device = topic.split("/")[2]
            for modbus_attr in message:
                self.timestamp = message[modbus_attr]["timestamp"]   
                for data_point in message[modbus_attr]["value_batch"]
                    self.payload[message[modbus_attr]["value_batch"][data_point]["name"]] = message[modbus_attr]["value_batch"][data_point]["value"]
                    if self.debug == True:
                        print(self.timestamp, self.payload)
                self.send_http()
        except Exception as e:
            print(datetime.datetime.now(), "- (MQTT) Could not read values from Message: ", message, e)
 
        modbus_attribute =         # get the last item of the topic branch, which is the name of the modbus-attribute
        self.timestamp = next(iter(message.values()))["timestamp"]       # get timestamp-value
        value_batch = message[modbus_attribute]["value_batch"]
        self.payload = {}
        for modbus_number in value_batch:
            self.payload[value_batch[modbus_number]["name"]] = value_batch[modbus_number]["value"]
        self.send_http()

    def connect_mqtt(self):
        try:
            print(datetime.datetime.now(), "- (MQTT) Connecting to Host: ", self.host)
            self.client.username_pw_set(self.username, self.password)
            if self.tls == True:
                self.client.tls_set(
                    ca_certs = None,                        
                    certfile = None,
                    keyfile = None,
                    cert_regs = ssl.CERT_REQUIRED,
                    tls_version = ssl.PROTOCOL_TLSv1_2,
                    ciphers = None,
                )
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.loop_start()                 # Make sure reconnect is handled automatically
            self.client.connet(self.host, self.port, 60)
            self.client.subscribe(self.sub_topic)
            print(datetime.datetime.now(), "- (MQTT) Subscribed to topic: ", self.sub_topic)
            #return client

        except Exception as e:
            print(datetime.datetime.now(), "- (MQTT) Could not connect to MQTT with Error: ", e)

def main(username, password, host, port, tls, sub_topic, debug, iota_endpoint, api_key):
    mqtt_adapter = GlendimplexAdapter(username, password, host, port, tls, sub_topic, debug, iota_endpoint, api_key)
    mqtt_adapter.connect_mqtt()

if __name__ == "__main__":
    main(username, password, host, port, tls, sub_topic, debug, iota_endpoint, api_key)
    

