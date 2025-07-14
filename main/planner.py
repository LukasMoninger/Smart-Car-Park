import subprocess
import os
import time
import grovepi

from actuators import *
from sensors import *


class Planner:

    def __init__(self):
        self.act_controller = Actuators()
        self.sen_controller = Sensors()
        self.act_controller.switch_light_green()

    def start_planner(self):
        interval = 2
        while True:
            domain = "../pddl/domain.pddl"
            problem = self.generate_problem()
            plan = self.generate_plan(domain, problem)
            print("Generated Plan of length ", len(plan))
            print("Plan:", plan)
            self.execute_plan(plan)
            time.sleep(interval)

    def generate_problem(self):
        text = """(define (problem smart_car_park_problem)
      (:domain smart_car_park)
      (:objects
        g1 - green_light
        r1 - red_light
        u1 - ultrasonic_entrance
        l1 - light_sensor
      )
      (:init"""

        if self.act_controller.status_green_led:
            text += "\n    (green_on g1)"
        else:
            text += "\n    (green_off g1)"
        if self.act_controller.status_red_led:
            text += "\n    (red_on r1)"
        else:
            text += "\n    (red_off r1)"

        distance = self.sen_controller.read_ultrasonic()
        if distance < 15:
            text += "\n    (detected u1)"
        else:
            text += "\n    (not_detected u1)"

        brightness = self.sen_controller.read_brightness()
        if brightness > 200:
            text += "\n    (bright l1)"
        else:
            text += "\n    (dark l1)"

        text += """\n  )
      (:goal
        (and"""

        if self.act_controller.status_green_led:
            text += "\n      (green_off g1)"
        else:
            text += "\n      (green_on g1)"
        if self.act_controller.status_red_led:
            text += "\n      (red_off r1)"
        else:
            text += "\n      (red_on r1)"
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
        cmd = ["pyperplan", domain, problem]
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


if __name__ == "__main__":
    planner = Planner()
    planner.start_planner()
