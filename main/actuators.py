import grovepi


class Actuators:

    def __init__(self):
        self.green_led = 3
        self.red_led = 2

        self.status_green_led = False
        self.status_red_led = False

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
