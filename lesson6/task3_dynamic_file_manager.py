from psutil import disk_partitions
from os import listdir, path as os_path, chdir, system, readlink, mkdir, symlink
from typing import Union, Optional


class ConsoleFileManager:
    def __init__(self):
        self.current_path = None

    @staticmethod
    def get_drives_letters() -> tuple:
        return tuple(drive.device[0] for drive in disk_partitions())

    def change_drive(self, command: Union[tuple, list]) -> None:
        drives_letters = self.get_drives_letters()

        if len(command) > 1 and command[0] == "1" and command[1].upper()[0] in drives_letters:
            drive = command[1].upper()[0]
            chdir(f"{drive}:/")
            self.current_path = f"{drive}:/"
            return

        print("")

    def object_type(self, path: str, object_: Optional[str]) -> Optional[str]:
        object_path = self.get_clear_path(path, object_)

        print("PATH", object_path)
        if os_path.islink(object_path):
            print("link")
            return self.object_type("", self.get_link_path("", object_path))
        elif os_path.isabs(object_):
            print("abs")
            return "abs_path"
        elif os_path.isdir(object_path):
            print("dir")
            return "dir"
        elif os_path.isfile(object_path):
            print("file")
            return "file"
        print("Unknown", object_path)
        return None

    @staticmethod
    def command_extract_path(command: Union[tuple, list]) -> str:
        return ' '.join(command[1:])

    def get_link_path(self, path: str, link: str):
        return readlink(os_path.join(path, link))

    @staticmethod
    def get_clear_path(path: str, object_: str) -> str:
        path = os_path.join(path, object_).replace("\\", "/")
        return path[:-1] if path.endswith("/") else path

    def change_dir_or_start_file(self, command: Union[tuple, list]) -> None:
        if len(command) <= 1:
            return

        object_ = self.command_extract_path(command)

        object_type = self.object_type(self.current_path, object_)
        if object_type == "dir":
            dir_ = self.get_clear_path(self.current_path, object_)
            chdir(dir_)
            self.current_path = dir_
        elif object_type == "abs_path":
            self.current_path = self.get_clear_path(object_, "")
            chdir(self.current_path)
        elif object_type == "link":
            link_path = self.get_clear_path(self.get_link_path(self.current_path, object_))
            object_type = self.object_type(link_path, "")
            self.change_dir_or_start_file(command[0] + object_type)
        elif object_type == "file":
            system(f"start {object_}")

    def execute_command(self) -> None:  # TODO: @overload
        print("CURRENT PATH (DFL):", self.current_path)

        command = input("Enter command > ").split()
        if len(command) < 1:
            return
        elif command[0] == "5":
            print("Пока!")
            exit()
        elif command[0] == "1" and len(command) > 1:
            self.change_dir_or_start_file(command)
        elif command[0] == "2":
            path = self.get_clear_path(self.current_path, "")
            path = "/".join(path.split("/")[:-1])

            if path == "":
                self.current_path = None
                return

            chdir(path)
            self.current_path = path
        elif command[0] == "3":
            type_to_create = input("What type of object u want to create? (file/link/dir) > ")

            if type_to_create == "file":
                filename = input("Enter filename > ")
                open(filename, "x").close()
            elif type_to_create == "link":
                link_name, *path = input("Enter <link_name> <path> > ").split()
                path = self.get_clear_path("/".join(path), "")
                symlink(path, link_name)


    def execute_drive_command(self):
        print("CURRENT PATH (DR):", None)

        command = input("Enter command > ").split()
        if len(command) < 1:
            return
        elif command[0] == "5":
            print("Bye!")
            exit()
        elif command[0] == "1":
            path = self.get_clear_path(self.command_extract_path(command), "")
            if self.object_type("", path) == "abs_path":
                self.current_path = path
                chdir(path)
            else:
                self.change_drive(command)

    def dir(self):
        if self.current_path is None:
            drives_letters = [drive.device[0] for drive in disk_partitions()]
            print("\n".join(f"{drive_letter + ':/':<50} <drive>" for drive_letter in drives_letters))
            print("1 - Choose drive (1 <drive_letter>)    5 - Exit")
            self.execute_drive_command()
        else:
            print("\n".join(
                f"{object_:<50} <{self.object_type(self.current_path, object_)}>" for
                object_ in listdir(self.current_path)))
            print("1 - Choose/Execute (1 <file/dir/link>)   2 - Back    3 - Create    4 - Delete    5 - Exit")
            self.execute_command()


console_manager = ConsoleFileManager()
while True:
    console_manager.dir()
