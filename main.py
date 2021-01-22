import paho.mqtt.client as mqtt
import json
import time
import ssl
import os

username = os.environ['MQTT_USER']
password = os.environ['MQTT_PASSWORD']
host = os.environ['MQTT_HOST']
port = os.environ['MQTT_PORT']
tls = os.environ['TLS_BOOL']
