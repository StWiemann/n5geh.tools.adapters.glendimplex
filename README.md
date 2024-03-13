# MQTT to HTTP Bridge

This project provides a Python script to bridge MQTT messages to HTTP requests.

## Features

- **MQTT Client**: Subscribes to a specified MQTT topic and listens for incoming messages.
- **HTTP Sender**: Sends received MQTT messages as HTTP requests to a specified endpoint.
- **Environment Variable Configuration**: All configurations are managed via environment variables for easy deployment in containerized environments.
- **TLS Support**: Supports TLS for secure MQTT connections.
- **Logging**: Configurable logging levels for debugging and monitoring.

## Requirements

- Python 3.x
- `paho-mqtt`: For MQTT client functionality.
- `requests`: For sending HTTP requests.

You can install the required packages using pip:

```bash
pip install paho-mqtt requests
```

## Configuration

Configuration is done via environment variables. Below are the required environment variables:

- `MQTT_USER`: Username for MQTT broker authentication.
- `MQTT_PASSWORD`: Password for MQTT broker authentication.
- `MQTT_HOST`: The hostname or IP address of the MQTT broker.
- `MQTT_PORT`: The port on which the MQTT broker is running (default is 8883).
- `TLS_BOOL`: Whether to use TLS for MQTT connections (`true` or `false`).
- `SUB_TOPIC`: The MQTT topic to subscribe to.
- `IOTA_ENDPOINT`: The HTTP endpoint to which the data should be sent.
- `API_KEY`: API key for authenticating with the HTTP endpoint.
- `LOG_LEVEL`: Logging level (e.g., `DEBUG`, `INFO`, `ERROR`). Default is `INFO`.

## Usage

1. Ensure all required environment variables are set.
2. Run the script:

```bash
python main.py
```

The script will subscribe to the specified MQTT topic, listen for messages, and forward them as HTTP requests to the specified endpoint.

## Logging

The script uses Python's built-in logging module. You can adjust the logging level via the `LOG_LEVEL` environment variable to get more or less output for debugging purposes.

## Security Note

When using `TLS_BOOL=true`, ensure you have the necessary certificates in place for a secure connection to the MQTT broker. The script currently does not specify `ca_certs`, `certfile`, or `keyfile` for TLS connections, so you may need to modify the script if your setup requires these.

## License

This project is open source and available under the MIT License.