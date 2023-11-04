from sys import argv
from time import sleep

from psutil import process_iter

banned_processes = argv[1:]

with open("banned_apps.exe", encoding="UTF-8") as fl:
    banned_processes.extend(fl.read().splitlines())

banned_processes = tuple(filter(len, banned_processes))

with open("banned_apps.exe", "w+", encoding="UTF-8") as fl:
    fl.write("\n" + "\n".join(set(banned_processes)))

print("BANNED", banned_processes)

while True:
    for process in process_iter():
        try:
            if process.name() in banned_processes:
                process.kill()
        except Exception as e:
            print(e)

    sleep(60 * 5)
