import time
import grovepi
import subprocess

light_sensor = 0
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


def test_brightness():
    interval = 0.5
    duration = 10
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            brightness = grovepi.analogRead(light_sensor)
            print(f"Brightness: {brightness}")
            time.sleep(interval)
    except IOError as e:
        print(f"I/O-Error: {e}")


def generate_plan(domain, problem):
    cmd = ["pyperplan", domain, problem]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    lines = result.stdout.splitlines()
    plan = []
    for line in lines:
        if line.strip().startswith("1:"):
            action = line.split(":", 1)[1].split("[")[0].strip()
            plan.append(action)
    return plan


def execute_plan(plan):
    for step in plan:
        print("Execute:", step)
        name, *args = step.strip("()").split()
        if name == "move":
            robot, src, dst = args
            move(robot, src, dst)


def move(robot, src, dst):
    print(f"Robot {robot} moves from {src} to {dst}")


def test_pddl():
    domain = "../pddl/domain_example.pddl"
    problem = "../pddl/problem_example.pddl"
    plan = generate_plan(domain, problem)
    execute_plan(plan)


if __name__ == "__main__":
    setup()
    # test_led(red_led)
    # test_led(green_led)
    # test_ultrasonic()
    # test_brightness()
    test_pddl()
