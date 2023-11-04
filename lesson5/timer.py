from sys import argv
from subprocess import run
from time import sleep

timer = float(argv[1])
while timer > 0:
    timer -= 0.1
    if timer > 0:
        print(f"\r{timer:.2f}", end="")
        sleep(0.1)
    else:
        print("\r0.00")

# print("end")
run(f"shutdown -s")
