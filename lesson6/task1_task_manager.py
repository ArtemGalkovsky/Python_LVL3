from colorama import Fore, Back, Style
import psutil as pu
import os
from datetime import datetime
from os import system


def bytes2gb(bytes_: int) -> float:
    return round(bytes_ / 1024 / 1024 / 1024, 3)


def run_once() -> None:
    print("\r")
    task_manager_text = f"""    TIME: {datetime.now().strftime("%m.%d.%Y, %H:%M:%S")} 
    OC: {os.name.upper()}, USER_NAME: {os.getlogin()}
    CPU: {pu.cpu_percent(1)}%, {pu.cpu_freq().current} MHz with {pu.cpu_count()} logical cores [{pu.cpu_count(logical=False)} real cores]!
    RAM: total={bytes2gb(pu.virtual_memory().total)}GB, available={bytes2gb(pu.virtual_memory().available)}GB percent={pu.virtual_memory().percent}, used={bytes2gb(pu.virtual_memory().used)}GB, free={bytes2gb(pu.virtual_memory().free)}GB

"""

    processes = [process for process in pu.process_iter()]

    index = 1
    task_manager_text += f"    {'PID':<7} | {'NAME':<30} | {'CPU':<20} | RAM\n"
    for process in processes:
        try:
            task_manager_text += f"    {str(process.pid):<7} | {process.name()[:25]:<30} | {f'{round(process.cpu_percent(), 3)}%':<20} | {process.memory_percent():.3f}%\n"
            index += 1
        except Exception as e:
            pass

        if index > 10:
            break

    system("cls")
    print(task_manager_text)


if __name__ == "__main__":
    while True:
        run_once()
    input()
