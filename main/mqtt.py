import json
from datetime import datetime

import paho.mqtt.client as mqtt


class MQTT:

    def __init__(self):
        self.MQTT_BROKER = "localhost"
        self.MQTT_PORT = 1883
        self.MQTT_TOPIC = "esp1/sensor/#"

        self.co2_level = 0

        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "raspi-sensor-reader")
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._running = False

    def start(self):
        try:
            self._client.connect(self.MQTT_BROKER, self.MQTT_PORT, keepalive=60)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            return

        self._client.loop_start()
        self._running = True

    def stop(self):
        if self._running:
            self._client.loop_stop()
            self._client.disconnect()
            self._running = False

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[{datetime.now()}] Connected with MQTT-Broker")
            client.subscribe(self.MQTT_TOPIC)
            print(f"[{datetime.now()}] Subscribe to topic '{self.MQTT_TOPIC}'")
        else:
            print(f"[{datetime.now()}] Connection failed, code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
        except Exception as e:
            print(f"[{datetime.now()}] Error parsing message: {e}")
            print(f"  Topic: {msg.topic}  Payload: {msg.payload!r}")
            return

        if msg.topic.endswith("co2"):
            self.co2_level = data.get('eCO2')
            print(f"[{datetime.now()}] CO2: {data.get('eCO2')} ppm  ")
        elif msg.topic.endswith("tvoc"):
            print(f"[{datetime.now()}] TVOC: {data.get('TVOC')} ppb  ")
        else:
            print(f"[{datetime.now()}] {msg.topic}: {data}")
