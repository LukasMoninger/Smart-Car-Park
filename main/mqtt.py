import json
import datetime
import time
import paho.mqtt.client as mqtt
from datetime import datetime


class MQTT:

    def __init__(self):
        self.MQTT_BROKER = "localhost"
        self.MQTT_PORT = 1883
        self.MQTT_TOPIC = "esp1/sensor/#"

        self.co2_level = 0

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "raspi-sensor-reader")
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        try:
            client.connect(self.MQTT_BROKER, self.MQTT_PORT, keepalive=60)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
            return

        client.loop_start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTerminate")
        finally:
            client.loop_stop()
            client.disconnect()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[{datetime.now()}] Verbunden mit MQTT-Broker")
            client.subscribe(self.MQTT_TOPIC)
            print(f"[{datetime.now()}] Abonniere Topic '{self.MQTT_TOPIC}'")
        else:
            print(f"[{datetime.now()}] Verbindung fehlgeschlagen, Code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
        except Exception as e:
            print(f"[{datetime.now()}] Fehler beim Parsen der Nachricht: {e}")
            print(f"  Topic: {msg.topic}  Payload: {msg.payload!r}")
            return

        if msg.topic.endswith("co2"):
            self.co2_level = data.get('eCO2')
            print(f"[{datetime.now()}] CO₂: {data.get('eCO2')} ppm  "
                  f"(T={data.get('T')}°C, RH={data.get('RH')}%)")
        elif msg.topic.endswith("tvoc"):
            print(f"[{datetime.now()}] TVOC: {data.get('TVOC')} ppb  "
                  f"(T={data.get('T')}°C, RH={data.get('RH')}%)")
        else:
            print(f"[{datetime.now()}] {msg.topic}: {data}")
