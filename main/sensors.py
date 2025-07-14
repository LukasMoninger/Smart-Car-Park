import grovepi


class Sensors:

    def __init__(self, mqtt_controller):
        self.mqtt_controller = mqtt_controller
        self.brightness_sensor = 0
        self.ultrasonic = 4

        self.brightness_limit = 200
        self.distance_limit = 15
        self.co2_limit = 800

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
        c02 = self.mqtt_controller.co2_level
        return c02

    def read_parking_occupancy(self):
        print("Parking Occupancy")
