import subprocess
import os
import time

from main.actuators import switch_light_green, switch_light_red


def generate_domain():
    domain = ""


def generate_plan(domain, problem):
    timeout = 5
    cmd = ["pyperplan", domain, problem]
    solution_file = problem + ".soln"

    if os.path.exists(solution_file):
        os.remove(solution_file)

    subprocess.run(cmd, check=True)
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
