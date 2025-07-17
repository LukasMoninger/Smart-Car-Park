import grovepi


class Sensors:

    def __init__(self, mqtt_controller):
        self.mqtt_controller = mqtt_controller
        self.brightness_sensor_port = 0
        self.ultrasonic_entrance_port = 4
        self.button_port = 5
        self.brightness_limit = 200
        self.co2_limit = 800
        self.distance_limit = 10
        grovepi.pinMode(self.button_port, "INPUT")

    def get_status_brightness(self):
        try:
            brightness = grovepi.analogRead(self.brightness_sensor_port)
            if brightness > self.brightness_limit:
                return True
            else:
                return False
        except IOError as e:
            print(f"I/O-Error: {e}")

    def get_status_co2(self):
        co2_level = self.mqtt_controller.co2_level
        if co2_level > self.co2_limit:
            return True
        else:
            return False

    def get_status_entrance(self):
        try:
            distance = grovepi.ultrasonicRead(self.ultrasonic_entrance_port)
            if distance < self.distance_limit:
                return True
            else:
                return False
        except IOError as e:
            print(f"I/O-Error: {e}")

    def get_status_button(self):
        try:
            state = grovepi.digitalRead(self.button_port)
            if state == 1:
                return True
            else:
                return False
        except IOError as e:
            print(f"I/O-Error: {e}")

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
