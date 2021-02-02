import paho.mqtt.client as mqtt
import json
import time
import ssl
import os
import datetime
import collections
import requests


# MQTT Configuration from Docker-Envs
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASSWORD')
host = os.getenv('MQTT_HOST')
str_port = os.getenv('MQTT_PORT', "8883")
str_tls = os.getenv('TLS_BOOL', "True")
sub_topic = os.getenv('SUB_TOPIC')
str_debug = os.getenv('DEBUG', "False")
iota_endpoint = os.getenv('IOTA_ENDPOINT')
api_key = os.getenv('API_KEY')

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
        headers = {'Content-Type': 'application/json'} 
        try:
            query_parameters = {"i": self.device, "t": datetime.datetime.utcfromtimestamp((self.timestamp/1000)).isoformat(), "k": self.api_key}      # i = fiware device ID, t = timestamp, k = API Key
            r = requests.post(self.iota_endpoint, headers = headers, data = json.dumps(self.payload), params = query_parameters)
            if self.debug == True:
                print(datetime.datetime.now(), "- (HTTP) Sent Values to IoT-Agent with Status: ", r.status_code)
                print("Query Parameters: ", query_parameters)
        except Exception as e:
            print(datetime.datetime.now(), "- (HTTP) Could not send Request with Error: ", e)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        if rc == 0:                                     # if successfully connected
            self.client.subscribe(self.sub_topic)
            print(datetime.datetime.now(), "- (MQTT) Subscribed to topic: ", self.sub_topic)
        else:
            print(datetime.datetime.now(), "- (MQTT) Failed to Connect to Broker")

    def on_message(self, client, userdata, msg):

        self.payload = {}
        if self.debug == True:
          print(msg.payload)
        try:
            message = json.loads(msg.payload)
            topic = msg.topic.lower()
            self.device = topic.split("/")[2]
            for modbus_attr in message:
                self.timestamp = message[modbus_attr]["timestamp"]   
                for data_point in message[modbus_attr]["value_batch"]:
                    self.payload[message[modbus_attr]["value_batch"][data_point]["name"]] = message[modbus_attr]["value_batch"][data_point]["value"]
                    if self.debug == True:
                        print(self.timestamp, self.payload)
                self.send_http()
        except Exception as e:
            print(datetime.datetime.now(), "- (MQTT) Could not read values from Message: ", message, e)

    def connect_mqtt(self):
        try:
            print(datetime.datetime.now(), "- (MQTT) Connecting to Host: ", self.host)
            self.client.username_pw_set(self.username, self.password)
            if self.tls == True:
                self.client.tls_set(
                    ca_certs = None,
                    certfile = None,
                    keyfile = None,
                    cert_reqs = ssl.CERT_REQUIRED,
                    tls_version = ssl.PROTOCOL_TLSv1_2,
                    ciphers = None,
                )
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
           # self.client.loop_start()                 # Make sure reconnect is handled automatically
            self.client.connect(self.host, self.port, 60)
            self.client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=True)
            #return client

        except Exception as e:
            print(datetime.datetime.now(), "- (MQTT) Could not connect to MQTT with Error: ", e)
            time.sleep(5)
            self.connect_mqtt()

def main():
    port = int(str_port)
    if str_tls == "True" or str_tls == "true":
        tls = True
    else:
        tls = False

    if str_debug == "True" or str_debug == "true":
        debug = True

    else:
        debug = False

    mqtt_adapter = GlendimplexAdapter(username, password, host, port, tls, sub_topic, debug, iota_endpoint, api_key)
    mqtt_adapter.connect_mqtt()
    while True:
      pass

if __name__ == "__main__":
    main()
    

