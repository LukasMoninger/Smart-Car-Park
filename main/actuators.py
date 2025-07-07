green_led = 3
red_led = 2


def switch_light_green():
    grovepi.digitalWrite(red_led, 0)
    grovepi.digitalWrite(green_led, 1)


def switch_light_red():
    grovepi.digitalWrite(green_led, 0)
    grovepi.digitalWrite(red_led, 1)
