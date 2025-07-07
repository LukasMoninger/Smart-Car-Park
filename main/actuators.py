green_led = 3
red_led = 2

status_green_led = 0
status_red_led = 0


def switch_light_green(self):
    grovepi.digitalWrite(red_led, 0)
    self.status_red_led = 0
    grovepi.digitalWrite(green_led, 1)
    self.status_green_led = 1


def switch_light_red(self):
    grovepi.digitalWrite(green_led, 0)
    self.status_green_led = 0
    grovepi.digitalWrite(red_led, 1)
    self.status_red_led = 1
