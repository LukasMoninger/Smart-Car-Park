import subprocess
import os
import time

from actuators import switch_light_green, switch_light_red, status_green_led, status_red_led
from sensors import read_ultrasonic


def start_planner():
    interval = 2
    while True:
        domain = "../pddl/domain.pddl"
        problem = generate_problem()
        plan = generate_plan(domain, problem)
        print("Generated Plan of length ", len(plan))
        print("Plan:", plan)
        execute_plan(plan)
        time.sleep(interval)


def generate_problem():
    text = """(define (problem smart_car_park_problem)
  (:domain smart_car_park)
  (:objects
    g1 - green_light
    r1 - red_light
    u1 - ultrasonic_entrance
  )
  (:init"""

    if status_green_led:
        text += "\n    (on_green g1)"
    else:
        text += "\n    (off_green g1)"
    if status_red_led:
        text += "\n    (on_red r1)"
    else:
        text += "\n    (off_red r1)"

    distance = read_ultrasonic()
    if distance < 20:
        text += "\n    (detected u1)"
    else:
        text += "\n    (not_detected u1)"

    text += """\n  )
  (:goal
    (and"""

    if status_green_led:
        text += "\n      (off_green g1)"
    else:
        text += "\n      (on_green g1)"
    if status_red_led:
        text += "\n      (off_red r1)"
    else:
        text += "\n      (on_red r1)"
    text += """\n    )
  )
)"""
    print(text)
    problem_file = "../pddl/smart_car_park_problem.pddl"
    with open(problem_file, "w") as file:
        file.write(text)
    return problem_file


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


def execute_plan(plan):
    for step in plan:
        print("Execute:", step)
        name, *args = step.strip("()").split()
        if name == "switch_light_green":
            switch_light_green()
        elif name == "switch_light_red":
            switch_light_red()
