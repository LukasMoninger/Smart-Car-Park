import grovepi
import threading
import notification


class Actuators:

    def __init__(self):
        self.green_led = 3
        self.red_led = 2
        grovepi.pinMode(self.green_led, "OUTPUT")
        grovepi.pinMode(self.red_led, "OUTPUT")

        self.status_green_led = False
        self.status_red_led = False
        self.status_ventilation = False
        self.status_brightness_signpost = True
        self.notification_sent = False
        self.status_timer = False

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

    def make_light_brighter(self):
        self.status_brightness_signpost = True
        print("Light made brighter")

    def make_light_darker(self):
        self.status_brightness_signpost = False
        print("Light made darker")

    def activate_signpost(self):
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
        notification.send_text_notification(text)
        self.notification_sent = True
        self.status_timer = False
        print(f"Notification sent")
