import grovepi


def read_ultrasonic():
    ultrasonic = 4
    try:
        distance = grovepi.ultrasonicRead(ultrasonic)
        return distance
    except IOError as e:
        print(f"I/O-Error: {e}")
