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

    def get_status_brightness(self):
        brightness = self.read_brightness()
        if brightness > self.brightness_limit:
            return True
        else:
            return False

    def read_ultrasonic(self):
        try:
            distance = grovepi.ultrasonicRead(self.ultrasonic)
            return distance
        except IOError as e:
            print(f"I/O-Error: {e}")

    def read_co2(self):
        c02 = self.mqtt_controller.co2_level
        print(f"CO2 Level: {c02}")
        return c02

    def get_status_co2(self):
        co2 = self.read_co2()
        if co2 > self.co2_limit:
            return True
        else:
            return False

    def read_button(self):
        print("Button Pressed")

    def get_parking_occupancy(self):
        distance = self.mqtt_controller.distance
        if distance < 5:
            print("Parking space occupied")
            return True
        else:
            print("Parking space free")
            return False
