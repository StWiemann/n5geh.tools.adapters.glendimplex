import paho.mqtt.client as mqtt
import json
import time
import ssl
import os
import datetime
import requests
import logging


def str_to_bool(value):
    return str(value).lower() == "true"


# MQTT Configuration from Docker-Envs
username = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")
host = os.getenv("MQTT_HOST")
port = int(os.getenv("MQTT_PORT", 8883))
tls = str_to_bool(os.getenv("TLS_BOOL", True))
sub_topic = os.getenv("SUB_TOPIC")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
iota_endpoint = os.getenv("IOTA_ENDPOINT")
api_key = os.getenv("API_KEY")


# Set up logging
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


class GlendimplexAdapter:
    def __init__(
        self,
        username,
        password,
        host,
        port,
        tls,
        sub_topic,
        iota_endpoint,
        api_key,
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.tls = tls
        self.sub_topic = sub_topic
        self.iota_endpoint = iota_endpoint
        self.api_key = api_key

        self.client = mqtt.Client()
        self.timestamp = None
        self.payload = None
        self.device = None

    def send_http(self):
        headers = {"Content-Type": "application/json"}
        try:
            query_parameters = {
                "i": self.device,
                "t": datetime.datetime.utcfromtimestamp(
                    (self.timestamp / 1000)
                ).isoformat(),
                "k": self.api_key,
            }
            r = requests.post(
                self.iota_endpoint,
                headers=headers,
                data=json.dumps(self.payload),
                params=query_parameters,
            )

            logger.debug(
                "(HTTP) Sent Values to IoT-Agent with Status: %s", r.status_code
            )
            logger.debug("Query Parameters: %s", query_parameters)
        except Exception as e:
            logger.error("(HTTP) Could not send Request. Error: %s", e)

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code %s", rc)
        if rc == 0:
            client.subscribe(self.sub_topic)
            logger.info("(MQTT) Subscribed to topic: %s", self.sub_topic)

    def on_message(self, client, userdata, message):
        try:
            message = json.loads(message.payload)
            self.timestamp = message["timestamp"]
            self.device = message["device_id"]
            self.payload = {}
            for modbus_attr in message:
                if modbus_attr != "timestamp" and modbus_attr != "device_id":
                    for data_point in message[modbus_attr]["value_batch"]:
                        self.payload[
                            message[modbus_attr]["value_batch"][data_point]["name"]
                        ] = message[modbus_attr]["value_batch"][data_point]["value"]

                    logger.debug(
                        "Timestamp: %s, Payload: %s", self.timestamp, self.payload
                    )
                self.send_http()
        except Exception as e:
            logger.error(
                "(MQTT) Could not read values from Message: %s. Error: %s", message, e
            )

    def connect_mqtt(self):
        try:
            logger.info("(MQTT) Connecting to Host: %s", self.host)
            self.client.username_pw_set(self.username, self.password)
            if self.tls:
                self.client.tls_set(
                    ca_certs=None,
                    certfile=None,
                    keyfile=None,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2,
                    ciphers=None,
                )
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.host, self.port, 60)
            self.client.loop_forever(
                timeout=1.0, max_packets=1, retry_first_connection=True
            )

        except Exception as e:
            logger.error("(MQTT) Could not connect to MQTT. Error: %s", e)
            time.sleep(5)
            self.connect_mqtt()


def main():
    # Validate essential environment variables
    essential_vars = [
        "MQTT_USER",
        "MQTT_PASSWORD",
        "MQTT_HOST",
        "SUB_TOPIC",
        "IOTA_ENDPOINT",
        "API_KEY",
    ]
    missing_vars = [var for var in essential_vars if os.getenv(var) is None]
    if missing_vars:
        logger.error(
            "Missing essential environment variables: %s", ", ".join(missing_vars)
        )
        return

    mqtt_adapter = GlendimplexAdapter(
        username, password, host, port, tls, sub_topic, iota_endpoint, api_key
    )
    mqtt_adapter.connect_mqtt()


if __name__ == "__main__":
    main()
