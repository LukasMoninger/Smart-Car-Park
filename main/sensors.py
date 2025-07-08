import grovepi


class Sensors:

    def __init__(self):
        self.ultrasonic = 4

    def read_ultrasonic(self):
        try:
            distance = grovepi.ultrasonicRead(self.ultrasonic)
            return distance
        except IOError as e:
            print(f"I/O-Error: {e}")
