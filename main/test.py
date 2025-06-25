import time
import grovepi

red_led = 2
green_led = 3
ultrasonic = 4


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


if __name__ == "__main__":
    setup()
    test_led(red_led)
    test_led(green_led)
    test_ultrasonic()
