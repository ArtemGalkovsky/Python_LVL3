from psutil import disk_partitions
from os import listdir, path as os_path, system, mkdir, symlink, unlink
system("pip install Send2Trash")
from send2trash import send2trash
from typing import Union, Optional
from LnkParse3 import lnk_file


class ConsoleFileManager:
    def __init__(self) -> None:
        self.__current_path = None

    @property
    def current_path(self) -> str:
        return self.__current_path

    @current_path.setter
    def current_path(self, path: Optional[str]) -> None:
        if not path:
            self.__current_path = None
        elif os_path.exists(path):
            self.__current_path = path

    def get_dir_objects(self) -> tuple[dict[str, str], ...]:
        objects = []
        for object_name in listdir(self.current_path):
            object_path = os_path.join(self.current_path, object_name)
            object_type = self.get_type(object_path)

            objects.append({"name": object_name, "type": object_type, "path": object_path})

        return tuple(objects)

    @staticmethod
    def get_type(object_path: str) -> str:
        if os_path.islink(object_path):
            return "link"
        elif os_path.isdir(object_path):
            return "dir"
        elif os_path.isfile(object_path):
            if object_path[-4:] == ".lnk":
                return "link"

            return "file"
        return "Unknown"

    def create(self, type_: str) -> str:
        name = input("Enter name > ")
        path = f"{self.current_path}/{name}"

        if type_ == "dir":
            mkdir(path)
            return "Successfully created directory"
        elif type_ == "file":
            open(path, "x").close()
            return "Successfully created file"
        elif type_ == "link":
            link_real_path = input("Enter link real path in abs format (<drive>:/<path>) > ")
            symlink(link_real_path, name)
            return "Successfully created link"

    def object_redirector(self, object_path: str) -> Optional[str]:
        object_type = self.get_type(object_path)

        if object_type == "dir":
            self.current_path = object_path
            return "Successfully moved to new dir"
        elif object_type == "file":
            system(f"start {object_path}")
            return "Successfully started file"
        elif object_type == "link":
            with open(object_path) as fl:
                link_data = lnk_file(fl)
                return self.object_redirector(link_data.lnk_command)

        return "Incorrect path"

    def delete(self, path_to_object: str, object_type: str) -> Optional[str]:
        if object_type == "file":
            send2trash(path_to_object)
            return "Successfully removed file"
        elif object_type == "dir":
            send2trash(path_to_object)
            return "Successfully removed directory"
        elif object_type == "link":
            unlink(path_to_object)
            return "Successfully removed link"


    def execute_command(self, command: str) -> Optional[str]:
        if len(command) < 1:
            return "No command found"

        command, object_ = command[0], command.replace(" ", "", 1)[1:]
        object_ = object_.replace("/", "").replace("\\", "")

        if command == "5":
            exit(0)
        elif command == "4":
            object_path = f"{self.current_path}\\{object_}"
            object_type = self.get_type(object_path)
            return self.delete(object_path, object_type)

        elif command == "3" and self.current_path is not None:
            type_to_create = input("Enter type to create (file/link/dir) > ")
            return self.create(type_to_create)
        elif command == "2" and self.current_path is not None:
            split_path = self.current_path.split("/")
            self.current_path = "/".join(split_path[:-1])
            return "Successfully returned back"
        elif command == "1":
            if self.current_path is None:
                if object_[0] in (drive.device[0] for drive in disk_partitions()):
                    self.current_path = object_
                    return "Successfully changed drive"

                return "Incorrect drive path"

            object_path = f"{self.current_path}\\{object_}"
            return self.object_redirector(object_path)

        return "Unknown command"

    def dir(self, previous_command_output: Optional[str] = None) -> Optional[str]:
        if self.current_path is None:
            print("\n".join(f"{drive.device[:-1]:<50} <drive>" for drive in disk_partitions()))
            print("CURRENT PATH:", self.current_path)
            print("Command output:", previous_command_output)
            print("1 - Select    5 - Exit")
        else:
            for object_ in self.get_dir_objects():
                print(f"{object_['name'][:45]:<50} <{object_['type'] + '>':<30} {object_['path']}")

            print("CURRENT PATH:", self.current_path)
            print("Command output:", previous_command_output)
            print("1 - Select/Execute (1 <file/dir/link>)   2 - Back    3 - Create    4 - Delete (4 <file/dir/link>)    5 - Exit")


def main() -> None:
    console_manager = ConsoleFileManager()
    previous_command_output = None
    while True:
        try:
            console_manager.dir(previous_command_output)
            command = input("Enter command > ")
            previous_command_output = console_manager.execute_command(command)
        except Exception as e:
            previous_command_output = e


if __name__ == "__main__":
    main()
