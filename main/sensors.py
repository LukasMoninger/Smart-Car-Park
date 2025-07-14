import grovepi


class Sensors:

    def __init__(self):
        self.brightness_sensor = 0
        self.ultrasonic = 4

    def read_brightness(self):
        try:
            brightness = grovepi.analogRead(self.brightness_sensor)
            return brightness
        except IOError as e:
            print(f"I/O-Error: {e}")

    def read_ultrasonic(self):
        try:
            distance = grovepi.ultrasonicRead(self.ultrasonic)
            return distance
        except IOError as e:
            print(f"I/O-Error: {e}")

    def read_co2(self):
        try:
            c02 = -1
            return c02
        except IOError as e:
            print(f"I/O-Error: {e}")

    def read_parking_occupancy(self):
        print("Parking Occupancy")
