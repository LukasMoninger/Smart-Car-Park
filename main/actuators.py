import grovepi


class Actuators:

    def __init__(self):
        self.green_led = 3
        self.red_led = 2
        grovepi.pinMode(self.green_led, "OUTPUT")
        grovepi.pinMode(self.red_led, "OUTPUT")

        self.status_green_led = False
        self.status_red_led = False
        self.status_ventilation = False
        self.status_signpost_brightness = True

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
        self.status_signpost_brightness = True
        print("Light made brighter")

    def make_light_darker(self):
        self.status_signpost_brightness = False
        print("Light made darker")

    def send_notification(self):
        # Placeholder for notification logic
        print(f"Notification sent")