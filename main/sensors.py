import grovepi


class Sensors:

    def __init__(self, mqtt_controller):
        self.mqtt_controller = mqtt_controller
        self.brightness_sensor = 0
        self.ultrasonic = 4
        self.button = 5

        grovepi.pinMode(self.button, "INPUT")

        self.brightness_limit = 200
        self.distance_limit = 10
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

    def get_status_entrance(self):
        distance = self.read_ultrasonic()
        if distance < self.distance_limit:
            return True
        else:
            return False

    def get_status_co2(self):
        co2_level = self.mqtt_controller.co2_level
        if co2_level > self.co2_limit:
            return True
        else:
            return False

    def get_status_button(self):
        try:
            state = grovepi.digitalRead(self.button)
            if state == 1:
                return True
            else:
                return False
        except IOError:
            print("I/O-Error while reading button state")

    def get_parking_occupancy(self, parking_space):
        if parking_space == 1:
            distance = self.mqtt_controller.distance
            if distance < 5:
                print("Parking space 1 occupied, distance:", distance)
                return True
            else:
                print("Parking space 1 free, distance:", distance)
                return False
        else:
            return False
