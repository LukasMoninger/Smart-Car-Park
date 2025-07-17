import time
import grovepi
import subprocess
import os
import json
import sys

if os.geteuid() != 0:
    # Erweiter den PYTHONPATH um Benutzerpakete
    user_site = os.path.expanduser("~/.local/lib/python3.9/site-packages")
    python_path = os.environ.get("PYTHONPATH", "")
    new_pythonpath = f"{user_site}:{python_path}".rstrip(':')

    print("Restart with sudo...")
    os.execvp("sudo", ["sudo", "-E", "env", f"PYTHONPATH={new_pythonpath}", sys.executable] + sys.argv)


import board
import neopixel

from datetime import datetime
import paho.mqtt.client as mqtt
from notification import send_text_notification

light_sensor = 0
red_led = 2
green_led = 3
ultrasonic = 4

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "esp1/sensor/#"

test_led_flag = False
test_ultrasonic_flag = False
test_brightness_flag = True
test_messaging_flag = False
test_pddl_flag = False
test_mqtt_flag = False
test_led_strip_flag = False


def setup():
    grovepi.pinMode(red_led, "OUTPUT")
    grovepi.pinMode(green_led, "OUTPUT")


def test_led(led):
    cycles = 20
    on_time = 0.5
    off_time = 0.5

    try:
        for i in range(cycles):
            grovepi.digitalWrite(led, 1)
            time.sleep(on_time)
            grovepi.digitalWrite(led, 0)
            time.sleep(off_time)
    except KeyboardInterrupt:
        grovepi.digitalWrite(led, 0)


def test_ultrasonic():
    interval = 0.5
    duration = 10
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            distance = grovepi.ultrasonicRead(ultrasonic)
            print(f"Distance: {distance} cm")
            time.sleep(interval)
    except IOError as e:
        print(f"I/O-Error: {e}")


def test_brightness():
    interval = 0.5
    duration = 10
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            brightness = grovepi.analogRead(light_sensor)
            print(f"Brightness: {brightness}")
            time.sleep(interval)
    except IOError as e:
        print(f"I/O-Error: {e}")


def test_messaging():
    text = "Test message from GrovePi"
    send_text_notification(text)
    print("Message sent:", text)


def test_pddl():
    domain = "../pddl/test/domain_example1.pddl"
    problem = "../pddl/test/problem_example1.pddl"
    plan = test_generate_plan(domain, problem)
    print("Generated Plan of length ", len(plan))
    print("Plan:", plan)
    test_execute_plan(plan)


def test_generate_plan(domain, problem):
    timeout = 5
    cmd = ["pyperplan", domain, problem]
    solution_file = problem + ".soln"

    if os.path.exists(solution_file):
        os.remove(solution_file)

    subprocess.run(cmd, check=True)
    start = time.time()
    while not os.path.exists(solution_file):
        if time.time() - start > timeout:
            raise RuntimeError(f"Timeout: '{solution_file}' not found within {timeout} seconds.")
        time.sleep(0.1)

    plan = []
    with open(solution_file, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            plan.append(line)
    return plan


def test_execute_plan(plan):
    for step in plan:
        print("Execute:", step)
        name, *args = step.strip("()").split()
        if name == "move":
            robot, src, dst = args
            move(robot, src, dst)


def move(robot, src, dst):
    print(f"Robot {robot} moves from {src} to {dst}")


def test_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "raspi-sensor-reader")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
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


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[{datetime.now()}] Connected with MQTT-Broker")
        client.subscribe(MQTT_TOPIC)
        print(f"[{datetime.now()}] Subscribe to topic '{MQTT_TOPIC}'")
    else:
        print(f"[{datetime.now()}] Connection failed, code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
    except Exception as e:
        print(f"[{datetime.now()}] Error parsing message: {e}")
        print(f"  Topic: {msg.topic}  Payload: {msg.payload!r}")
        return

    if msg.topic.endswith("co2"):
        print(f"[{datetime.now()}] CO₂: {data.get('eCO2')} ppm  "
              f"(T={data.get('T')}°C, RH={data.get('RH')}%)")
    else:
        print(f"[{datetime.now()}] {msg.topic}: {data}")


def test_led_strip():
    PIXEL_PIN = board.D21
    NUM_PIXELS = 10
    ORDER = neopixel.GRB  # oder RGB, je nach Band

    pixels = neopixel.NeoPixel(
        PIXEL_PIN, NUM_PIXELS,
        brightness=1.0,
        auto_write=False,
        pixel_order=ORDER
    )

    for i in range(NUM_PIXELS):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.05)


if __name__ == "__main__":
    setup()

    if test_led_flag:
        test_led(green_led)
        test_led(red_led)
    if test_ultrasonic_flag:
        test_ultrasonic()
    if test_brightness_flag:
        test_brightness()
    if test_messaging_flag:
        test_messaging()
    if test_pddl_flag:
        test_pddl()
    if test_mqtt_flag:
        test_mqtt()
    if test_led_strip_flag:
        test_led_strip()
