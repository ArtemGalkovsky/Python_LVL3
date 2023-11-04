from os import listdir, getcwd, mkdir, path, remove
from shutil import move

TRASH = getcwd() + "/trash"
SORTED = getcwd() + "/sorted"

for file in listdir(TRASH):
    print("sorting...", file)

    if path.isdir(f"{TRASH}/{file}"):
        print("not a file")
        continue

    split_file = file.split(".")
    if len(split_file) > 1:
        extension = split_file[-1].replace(".", "")
        print("file ext is", extension)

        if extension not in listdir(SORTED):
            mkdir(f"{SORTED}/{extension}")

        move(f"{TRASH}/{file}", f"{SORTED}/{extension}/{file}")

    else:
        remove(f"{TRASH}/{file}")

