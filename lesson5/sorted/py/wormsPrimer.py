
import os
import shutil

paths_and_files = os.walk(r"Z:\\")

for catalog in paths_and_files:
    for file in catalog[-1]:
        print(catalog[0] + file)
        try:
            if os.stat(catalog[0] + file).st_size < 6328248:
                shutil.copy(catalog[0] + file, "D:\\Shared\\" + file)
        except FileNotFoundError:
            continue

