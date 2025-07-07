def read_ultrasonic():
    ultrasonic = 4
    try:
        distance = grovepi.ultrasonicRead(ultrasonic)
        print(f"Distance: {distance} cm")
        return distance
    except IOError as e:
        print(f"I/O-Error: {e}")
