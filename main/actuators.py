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

        self.status_green_led = False
        self.status_red_led = False
        self.status_ventilation = False
        self.status_brightness_signpost = True
        self.notification_sent = False
        self.status_timer = False

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
        print("Signpost activated")
        start_signpost = [0,4,8]
        end_signpost = [3,7,11]
        signpost = args[2]
        print("Signpost:", signpost)

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
            pixels[i] = (0, 255, 0)
            pixels.show()
            time.sleep(0.1)


    def deactivate_signpost(self, args):
        print("Signpost activated")

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
