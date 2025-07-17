import grovepi
import threading
import os
import time
import board
import neopixel

from twilio.rest import Client
from dotenv import load_dotenv


class Actuators:

    def __init__(self):
        self.green_led = 3
        self.red_led = 2
        grovepi.pinMode(self.green_led, "OUTPUT")
        grovepi.pinMode(self.red_led, "OUTPUT")

        load_dotenv()
        self._TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
        self._TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
        self._TWILIO_PHONE_SENDER = "+15137177026"
        self._TWILIO_PHONE_RECIPIENT = "+4915757086879"

        self._PIXEL_PIN = board.D21
        self._NUM_PIXELS = 45
        self._ORDER = neopixel.GRB
        self._pixels = neopixel.NeoPixel(
            self._PIXEL_PIN, self._NUM_PIXELS,
            brightness=1.0,
            auto_write=False,
            pixel_order=self._ORDER
        )

        self.status_green_led = False
        self.status_red_led = False
        self.status_ventilation = False
        self.status_brightness_signpost = True
        self.notification_sent = False
        self.status_timer = False

        self.status_signpost1 = False
        self.status_signpost2 = False
        self.status_signpost3 = False

        self.switch_light_red()

    def switch_light_green(self):
        grovepi.digitalWrite(self.red_led, 0)
        self.status_red_led = False
        grovepi.digitalWrite(self.green_led, 1)
        self.status_green_led = True

    def switch_light_red(self):
        grovepi.digitalWrite(self.green_led, 0)
        self.status_green_led = False
        grovepi.digitalWrite(self.red_led, 1)
        self.status_red_led = True

    def activate_ventilation(self):
        self.status_ventilation = True
        print("Ventilation activated")

    def deactivate_ventilation(self):
        self.status_ventilation = False
        print("Ventilation deactivated")

    def make_signpost_brighter(self, args):
        self.status_brightness_signpost = True
        print("Signpost made brighter")

    def make_signpost_darker(self, args):
        self.status_brightness_signpost = False
        print("Signpost made darker")

    def activate_signpost(self, args):
        signpost = args[2]
        print("Signpost:", signpost)

        if signpost == "s1":
            self.status_signpost1 = True
            self.activate_pixels(0, 10, (100, 100, 100))
            self.activate_pixels(30, 35, (100, 100, 100))
        elif signpost == "s2":
            self.status_signpost2 = True
            self.activate_pixels(10, 20, (100, 100, 100))
            self.activate_pixels(35, 40, (100, 100, 100))
        elif signpost == "s3":
            self.status_signpost3 = True
            self.activate_pixels(20, 30, (100, 100, 100))
            self.activate_pixels(40, 45, (100, 100, 100))

    def activate_pixels(self, start, end, color):
        for i in range(start, end):
            self._pixels[i] = color
            self._pixels.show()
            time.sleep(0.1)

    def deactivate_signpost(self, args):
        signpost = args[2]
        print("Signpost:", signpost)

        if signpost == "s1":
            self.status_signpost1 = False
            self.activate_pixels(0, 10, (0, 0, 0))
            self.activate_pixels(30, 35, (0, 0, 0))
        elif signpost == "s2":
            self.status_signpost2 = False
            self.activate_pixels(10, 20, (0, 0, 0))
            self.activate_pixels(35, 40, (0, 0, 0))
        elif signpost == "s3":
            self.status_signpost3 = False
            self.activate_pixels(20, 30, (0, 0, 0))
            self.activate_pixels(40, 45, (0, 0, 0))

    def start_timer(self):
        timer_duration = 60.0
        timer = threading.Timer(timer_duration, self.timer_expired)
        timer.start()

    def timer_expired(self):
        self.status_timer = True
        print("Timer expired!")

    def send_notification(self):
        text = "Parking time exceeded. Please move your car."
        print("Using account SID:", self._TWILIO_ACCOUNT_SID)
        print("Using auth token:", self._TWILIO_AUTH_TOKEN)

        client = Client(self._TWILIO_ACCOUNT_SID, self._TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=self._TWILIO_PHONE_RECIPIENT,
            from_=self._TWILIO_PHONE_SENDER,
            body=text)
        self.notification_sent = True
        self.status_timer = False
        print(f"Notification sent")
