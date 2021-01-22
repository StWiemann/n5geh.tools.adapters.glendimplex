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
iota_host = os.environ['IOTA_HOST']

class GlendimpleyAdapter:

    def __init__(self, username, password, host, port, tls, sub_topic, debug, iota_host)

    def send_http(timestamp, payload):

    def on_connect(rc):

        if rc == 0:
            print(datetime.datetime.now(), "- (MQTT) connected")

        else:
            print(datetime.datetime.now(), "- (MQTT) Connection Error: ", rc)

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload)
        topic = msg.topic
        #modbus_attribute =         # get the last item of the topic branch, which is the name of the modbus-attribute
        timestamp = next(iter(message.values()))["timestamp"]       # get timestamp-value
        value_batch = message[modbus_attribute]["value_batch"]
        payload = {}
        for modbus_number in value_batch:
            payload[value_batch[modbus_number]["name"]] = value_batch[modbus_number]["value"]

    def connect_mqtt(self, username, password, host, port, tls, sub_topic):
        try:
            print(print(datetime.datetime.now(), "- (MQTT) Connecting to Host: ", host)
            client = mqtt.Client()
            client.username_pw_set(username, password)
            if tls = true:
                client.tls_set(
                    ca_certs = None,
                    certfile = None,
                    keyfile = None,
                    cert_regs = ssl.CERT_REQUIRED
                    tls_version = ssl.PROTOCOL_TLSv1_2,
                    ciphers = None,
                )
            client.on_connect = on_connect
            client.on_message = on_message
            client.loop_start()                 # Make sure reconnect is handled automatically
            client.connet(host, port, 60)
            client.subscribe(sub_topic)
            print(datetime.datetime.now(), "- (MQTT) Subscribed to topic: ", sub_topic)
            #return client

        except Exception as e:
            print(datetime.datetime.now(), "- (MQTT) Could not connect to MQTT with Error: ", e)


    

