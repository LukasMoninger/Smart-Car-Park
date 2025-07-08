import grovepi

green_led = 3
red_led = 2

status_green_led = False
status_red_led = False


def switch_light_green():
    global status_green_led, status_red_led
    grovepi.digitalWrite(red_led, 0)
    status_red_led = False
    grovepi.digitalWrite(green_led, 1)
    status_green_led = True


def switch_light_red():
    global status_green_led, status_red_led
    grovepi.digitalWrite(green_led, 0)
    status_green_led = False
    grovepi.digitalWrite(red_led, 1)
    status_red_led = True
