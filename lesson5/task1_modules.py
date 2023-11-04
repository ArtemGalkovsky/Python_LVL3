from os import mkdir, chdir, getcwd, rename, remove
from shutil import move, rmtree

ROOT_DIR = getcwd() + "/root_dir"

mkdir(ROOT_DIR)
chdir(ROOT_DIR)

for dir_name in ("dir_1", "dir_2", "dir_3", "dir_4"):
    dir_dir = f"{ROOT_DIR}/{dir_name}"

    mkdir(dir_dir)
    chdir(dir_dir)

    for text_filename in ("f_1.txt", "f_2.txt", "f_3.txt", "f_4.txt"):
        with open(f"{dir_dir}/{text_filename}", "w+") as fl:
            pass

    chdir(ROOT_DIR)

input("Все каталоги и файлы созданы! Для продолжения нажмите Enter")

rename(f"{ROOT_DIR}/dir_1/f_2.txt", f"{ROOT_DIR}/dir_1/f_1_2.txt")
move(f"{ROOT_DIR}/dir_2", f"{ROOT_DIR}/dir_1/dir_2")
rename(f"{ROOT_DIR}/dir_3/f_4.txt", f"{ROOT_DIR}/dir_3/f_3_4.txt")
move(f"{ROOT_DIR}/dir_4", f"{ROOT_DIR}/dir_3/dir_4")

input("Все перемещено и переименовано! Для продолжения нажмите Enter")

rmtree(f"{ROOT_DIR}/dir_3")
#remove(f"{ROOT_DIR}/dir_")
# где удалять файл f_1.txt?

print("dir_3 - удалён, f_1.txt - удалёН!")