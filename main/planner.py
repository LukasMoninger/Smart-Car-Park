import subprocess
import sys
import grovepi

from actuators import *
from sensors import *
from mqtt import *


class Planner:

    def __init__(self):
        self.act_controller = Actuators()
        self.mqtt_controller = MQTT()
        self.sen_controller = Sensors(self.mqtt_controller)
        self.mqtt_controller.start()

        self.status_green_led = self.act_controller.status_green_led
        self.status_green_led_last = self.status_green_led
        self.status_red_led = self.act_controller.status_red_led
        self.status_red_led_last = self.status_red_led
        self.status_brightness = self.sen_controller.get_status_brightness()
        self.status_brightness_last = self.status_brightness
        self.status_brightness_signpost = self.act_controller.status_brightness_signpost
        self.status_brightness_signpost_last = self.status_brightness_signpost
        self.status_ventilation = self.act_controller.status_ventilation
        self.status_ventilation_last = self.status_ventilation
        self.status_co2 = self.sen_controller.get_status_co2()
        self.status_co2_last = self.status_co2
        self.status_button = self.sen_controller.get_status_button()
        self.status_button_last = self.status_button
        self.status_timer = self.act_controller.status_timer
        self.status_timer_last = self.status_timer
        self.status_entrance = self.sen_controller.get_status_entrance()
        self.status_entrance_last = self.status_entrance

        self.status_signpost1 = self.act_controller.status_signpost1
        self.status_signpost1_last = self.status_signpost1
        self.status_signpost2 = self.act_controller.status_signpost2
        self.status_signpost2_last = self.status_signpost2
        self.status_signpost3 = self.act_controller.status_signpost3
        self.status_signpost3_last = self.status_signpost3
        self.status_parking1 = self.sen_controller.get_parking_occupancy(1)
        self.status_parking1_last = self.status_parking1
        self.status_parking2 = self.sen_controller.get_parking_occupancy(2)
        self.status_parking2_last = self.status_parking2
        self.status_parking3 = self.sen_controller.get_parking_occupancy(3)
        self.status_parking3_last = self.status_parking3

    def start_planner(self):
        interval = 4
        while True:
            if self.state_change_detected():
                domain = "../pddl/domain.pddl"
                problem = self.generate_problem()
                plan = self.generate_plan(domain, problem)
                print("Generated Plan of length ", len(plan))
                print("Plan:", plan)
                self.execute_plan(plan)
            time.sleep(interval)

    def state_change_detected(self):
        change = False
        self.status_green_led = self.act_controller.status_green_led
        if self.status_green_led != self.status_green_led_last:
            change = True
            self.status_green_led_last = self.status_green_led
            print("Status green changed")

        self.status_red_led = self.act_controller.status_red_led
        if self.status_red_led != self.status_red_led_last:
            change = True
            self.status_red_led_last = self.status_red_led
            print("Status red changed")

        self.status_brightness = self.sen_controller.get_status_brightness()
        if self.status_brightness != self.status_brightness_last:
            change = True
            self.status_brightness_last = self.status_brightness
            print("Brightness changed")

        self.status_brightness_signpost = self.act_controller.status_brightness_signpost
        if self.status_brightness_signpost != self.status_brightness_signpost_last:
            change = True
            self.status_brightness_signpost_last = self.status_brightness_signpost
            print("Signpost brightness changed")

        self.status_ventilation = self.act_controller.status_ventilation
        if self.status_ventilation != self.status_ventilation_last:
            change = True
            self.status_ventilation_last = self.status_ventilation
            print("Ventilation status changed")

        self.status_co2 = self.sen_controller.get_status_co2()
        if self.status_co2 != self.status_co2_last:
            change = True
            self.status_co2_last = self.status_co2
            print("CO2 level changed")

        self.status_button = self.sen_controller.get_status_button()
        if self.status_button != self.status_button_last:
            change = True
            self.status_button_last = self.status_button
            print("Button status changed")

        self.status_timer = self.act_controller.status_timer
        if self.status_timer != self.status_timer_last:
            change = True
            self.status_timer_last = self.status_timer
            print("Timer status changed")

        self.status_entrance = self.sen_controller.get_status_entrance()
        if self.status_entrance != self.status_entrance_last:
            change = True
            self.status_entrance_last = self.status_entrance
            print("Entrance status changed")

        self.status_signpost1 = self.act_controller.status_signpost1
        if self.status_signpost1 != self.status_signpost1_last:
            change = True
            self.status_signpost1_last = self.status_signpost1
            print("Signpost 1 status changed")

        self.status_signpost2 = self.act_controller.status_signpost2
        if self.status_signpost2 != self.status_signpost2_last:
            change = True
            self.status_signpost2_last = self.status_signpost2
            print("Signpost 2 status changed")

        self.status_signpost3 = self.act_controller.status_signpost3
        if self.status_signpost3 != self.status_signpost3_last:
            change = True
            self.status_signpost3_last = self.status_signpost3
            print("Signpost 3 status changed")

        self.status_parking1 = self.sen_controller.get_parking_occupancy(1)
        if self.status_parking1 != self.status_parking1_last:
            change = True
            self.status_parking1_last = self.status_parking1
            print("Parking 1 status changed")

        self.status_parking2 = self.sen_controller.get_parking_occupancy(2)
        if self.status_parking2 != self.status_parking2_last:
            change = True
            self.status_parking2_last = self.status_parking2
            print("Parking 2 status changed")

        self.status_parking3 = self.sen_controller.get_parking_occupancy(3)
        if self.status_parking3 != self.status_parking3_last:
            change = True
            self.status_parking3_last = self.status_parking3
            print("Parking 3 status changed")

        return change

    def generate_problem(self):
        text = """(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    e1 - entrance
    l1 - light_sensor
    c1 - co2_sensor
    v1 - ventilation
    s1 - signpost
    s2 - signpost
    s3 - signpost
    p1 - parking_space
    p2 - parking_space
    p3 - parking_space
  )
  (:init"""

        if self.status_green_led:
            text += "\n    (green_on g1)"
        else:
            text += "\n    (green_off g1)"
        if self.status_red_led:
            text += "\n    (red_on r1)"
        else:
            text += "\n    (red_off r1)"

        if self.status_entrance:
            text += "\n    (entrance_detected e1)"
        else:
            text += "\n    (entrance_not_detected e1)"

        if self.status_brightness:
            text += "\n    (bright l1)"
        else:
            text += "\n    (dark l1)"

        if self.status_brightness_signpost:
            text += "\n    (signpost_bright s1)"
            text += "\n    (signpost_bright s2)"
            text += "\n    (signpost_bright s3)"
        else:
            text += "\n    (signpost_dark s1)"
            text += "\n    (signpost_dark s2)"
            text += "\n    (signpost_dark s3)"

        if self.status_signpost1:
            text += "\n    (signpost_on s1)"
        else:
            text += "\n    (signpost_off s1)"

        if self.status_signpost2:
            text += "\n    (signpost_on s2)"
        else:
            text += "\n    (signpost_off s2)"

        if self.status_signpost3:
            text += "\n    (signpost_on s3)"
        else:
            text += "\n    (signpost_off s3)"

        if self.status_parking1:
            text += "\n    (parking_occupied p1)"
        else:
            text += "\n    (parking_free p1)"

        if self.status_parking2:
            text += "\n    (parking_occupied p2)"
        else:
            text += "\n    (parking_free p2)"

        if self.status_parking3:
            text += "\n    (parking_occupied p3)"
        else:
            text += "\n    (parking_free p3)"

        if self.status_ventilation:
            text += "\n    (ventilation_on v1)"
        else:
            text += "\n    (ventilation_off v1)"

        if self.status_co2:
            text += "\n    (co2_high c1)"
        else:
            text += "\n    (co2_low c1)"

        text += "\n    (connected s1 p1)"
        text += "\n    (connected s2 p2)"
        text += "\n    (connected s3 p3)"
        text += """\n  )
  (:goal
    (and """
        if self.status_red_led and self.status_entrance:
            text += "\n      (green_on g1)"
            text += "\n      (red_off r1)"
        else:
            text += "\n      (green_off g1)"
            text += "\n      (red_on r1)"

        if self.status_brightness:
            text += "\n      (signpost_bright s1)"
            text += "\n      (signpost_bright s2)"
            text += "\n      (signpost_bright s3)"
        else:
            text += "\n      (signpost_dark s1)"
            text += "\n      (signpost_dark s2)"
            text += "\n      (signpost_dark s3)"

        if self.status_co2:
            text += "\n      (ventilation_on v1)"
        else:
            text += "\n      (ventilation_off v1)"

        if self.status_green_led and not self.status_parking1:
            text += "\n      (signpost_on s1)"
        else:
            text += "\n      (signpost_off s1)"

        if self.status_green_led and not self.status_parking2:
            text += "\n      (signpost_on s2)"
        else:
            text += "\n      (signpost_off s2)"

        if self.status_green_led and not self.status_parking3:
            text += "\n      (signpost_on s3)"
        else:
            text += "\n      (signpost_off s3)"

        if self.status_green_led:
            if not self.status_parking1:
                text += "\n      (signpost_on s1)"
                text += "\n      (signpost_off s2)"
                text += "\n      (signpost_off s3)"
            elif not self.status_parking2:
                text += "\n      (signpost_off s1)"
                text += "\n      (signpost_on s2)"
                text += "\n      (signpost_off s3)"
            elif not self.status_parking3:
                text += "\n      (signpost_off s1)"
                text += "\n      (signpost_off s2)"
                text += "\n      (signpost_on s3)"
        else:
            text += "\n      (signpost_off s1)"
            text += "\n      (signpost_off s2)"
            text += "\n      (signpost_off s3)"

        text += """\n    )
  )
)"""
        print(text)
        problem_file = "../pddl/smart_car_park_problem.pddl"
        with open(problem_file, "w") as file:
            file.write(text)
        return problem_file

    @staticmethod
    def generate_plan(domain, problem):
        timeout = 5
        cmd = ["/home/pi/.local/bin/pyperplan", domain, problem]
        solution_file = problem + ".soln"

        if os.path.exists(solution_file):
            os.remove(solution_file)

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if output.endswith("No solution could be found"):
            print("No solution could be found")
            return []

        start = time.time()
        while not os.path.exists(solution_file):
            if time.time() - start > timeout:
                raise RuntimeError(f"Timeout: '{solution_file}' not found within {timeout} seconds.")
            time.sleep(0.1)

        plan = []
        with open(solution_file, "r") as file:
            for line in file:
                line = line.strip()
                print(line)
                if not line:
                    continue
                plan.append(line)
        return plan

    def execute_plan(self, plan):
        for step in plan:
            print("Execute:", step)
            name, *args = step.strip("()").split()
            if name == "switch_light_green":
                self.act_controller.switch_light_green()
            elif name == "switch_light_red":
                self.act_controller.switch_light_red()
            elif name == "activate_ventilation":
                self.act_controller.activate_ventilation()
            elif name == "deactivate_ventilation":
                self.act_controller.deactivate_ventilation()
            elif name == "make_signpost_brighter":
                self.act_controller.make_signpost_brighter(args)
            elif name == "make_signpost_darker":
                self.act_controller.make_signpost_darker(args)
            elif name == "start_timer":
                self.act_controller.start_timer()
            elif name == "send_notification":
                self.act_controller.send_notification()
            elif name == "activate_signpost":
                self.act_controller.activate_signpost(args)
            elif name == "deactivate_signpost":
                self.act_controller.deactivate_signpost(args)


if __name__ == "__main__":
    if os.geteuid() != 0:
        user_site = os.path.expanduser("~/.local/lib/python3.9/site-packages")
        python_path = os.environ.get("PYTHONPATH", "")
        new_python_path = f"{user_site}:{python_path}".rstrip(':')

        print("Restart with sudo...")
        os.execvp("sudo", ["sudo", "-E", "env", f"PYTHONPATH={new_python_path}", sys.executable] + sys.argv)

    planner = Planner()
    planner.start_planner()
