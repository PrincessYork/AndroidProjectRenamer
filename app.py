WELCOME_TEXT = """
Hi! This is the AndroidProjectRenamer script.
Type your text in the fields to change some
properties of your project.
!!!Don't forget to make a backup before doing it!!!
"""
DEFAULT_COLOR = "\033[;;m"
ERROR_COLOR = "\033[1;31;m"
SUCCESS_COLOR = "\033[1;32;m"
WARN_COLOR = "\033[1;33;m"
ACCENT_COLOR = "\033[1;36;m"

class AndroidProjectRenamerException(Exception):
    def __init__(self, what):
        self.what = what

    def __str__(self):
        return "AndroidProjectRenamerException: " + self.what


class AndroidProjectRenamer:

    project_path: str
    new_package: str
    old_package: str
    new_developer_link: str
    manifest_path: str
    ready_to_move: bool
    moved: bool

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.new_package = None
        self.old_package = None
        self.new_developer_link = None
        self.manifest_path = None
        self.ready_to_move = False
        self.moved = False

        if not self.is_project(project_path):
            raise AndroidProjectRenamerException("This is not a project")

        self.old_package = self.get_old_package()

    def set_new_package(self, package: str):
        import re
        package = package.lower()
        if re.match(r"^[a-z]+(\.[a-z]+)+$", package):
            if package != self.old_package:
                self.new_package = str(package)
            else: raise AndroidProjectRenamerException("This package name is already uses: " + package)
        else:
            raise AndroidProjectRenamerException("Incorrect package name: " + package)

    def get_old_package(self):
        import re
        manifest_path = self.project_path
        manifest_path = self.path_append(manifest_path, "app")
        manifest_path = self.path_append(manifest_path, "src")
        manifest_path = self.path_append(manifest_path, "main")

        try:
            with open(self.path_append(manifest_path, "AndroidManifest.xml")) as file:
                self.manifest_path = self.path_append(manifest_path, "AndroidManifest.xml")
                for line in file:
                    package_string = re.search(r"package=\"[a-z]+(\.[a-z]+)+\"", line)
                    if package_string is not None:
                        return str(re.search(r"[a-z]+(\.[a-z]+)+", package_string.group(0)).group(0))
                raise AndroidProjectRenamerException("No package name in path: " + manifest_path)
        except (OSError, FileNotFoundError):
            raise AndroidProjectRenamerException("AndroidManifest.xml not found in path: " + manifest_path)

    def is_project(self, project_path: str):
        if self.dir_contains(project_path, "app"):
            project_path = self.path_append(project_path, "app")
            if self.dir_contains(project_path, "src"):
                project_path = self.path_append(project_path, "src")
                if self.dir_contains(project_path, "main"):
                    return True
        return False

    @staticmethod
    def path_append(path: str, append: str):
        from sys import platform

        if platform == "win32":
            path_delimiter = "\\"
        else:
            path_delimiter = "/"

        append = str(append)
        if path.endswith(path_delimiter):
            path += append
        else:
            path += path_delimiter + append
        return path

    @staticmethod
    def dir_contains(path: str, var: str):
        import os
        try:
            var = str(var)
            if var in os.listdir(path):
                return True
            return False
        except:
            raise AndroidProjectRenamerException("Wrong path: " + path)

    def create_new_package_dirs(self):
        if self.new_package is None:
            raise AndroidProjectRenamerException("Can't create package dirs because new_package is None")

        import os

        def create_package_dirs(path: str, package_dir_list: list):
            # TODO: Выдаёт ошибку file exists когда новый пакет является укороченной версией старого
            path = self.path_append(path, "java")
            for directory in package_dir_list:
                path = self.path_append(path, directory)
            try:
                os.makedirs(path)
            except FileExistsError:
                raise AndroidProjectRenamerException("Files with this path already exists: " + path)

        path = self.project_path
        path = self.path_append(path, "app")
        path = self.path_append(path, "src")

        package_dir_list = str(self.new_package).split(".")

        if "androidTest" in os.listdir(path):
            create_package_dirs(self.path_append(path, "androidTest"), package_dir_list)

        if "test" in os.listdir(path):
            create_package_dirs(self.path_append(path, "test"), package_dir_list)

        if "main" in os.listdir(path):
            create_package_dirs(self.path_append(path, "main"), package_dir_list)

        self.ready_to_move = True

    def update_files_package(self):
        if not self.moved:
            raise AndroidProjectRenamerException("Files must be moved before updating package")

        path = self.project_path
        path = self.path_append(path, "app")
        path = self.path_append(path, "src")

        def update_package(path: str, part: str):
            path = self.path_append(path, part)
            package_dir_list = self.new_package.split(".")

            for directory in package_dir_list:
                path = self.path_append(path, directory)

            for file_name in os.listdir(path):
                lines = ""
                with open(self.path_append(path, file_name)) as file:
                    for line in file:
                        lines += line.replace(self.old_package, self.new_package)
                with open(self.path_append(path, file_name), 'w') as file:
                    file.writelines(lines)

        if "androidTest" in os.listdir(path):
            update_package(path, "androidTest")

        if "test" in os.listdir(path):
            update_package(path, "test")

        if "main" in os.listdir(path):
            update_package(path, "main")

    def update_manifest(self):
        lines = ""
        with open(self.manifest_path) as file:
            for line in file:
                lines += line.replace(self.old_package, self.new_package)
        with open(self.manifest_path, 'w') as file:
            file.writelines(lines)

    def move_files(self):
        if not self.ready_to_move:
            raise AndroidProjectRenamerException("Can't move files: new package dirs are not exist")

        import os
        import shutil

        def move(path: str, part: str):
            old_package_dir_list = self.old_package.split(".")

            src = self.path_append(path, part)
            src = self.path_append(src, "java")

            for directory in old_package_dir_list:
                src = self.path_append(src, directory)

            new_package_dir_list = str(self.new_package).split(".")

            dst = self.path_append(path, part)
            dst = self.path_append(dst, "java")

            for directory in new_package_dir_list:
                dst = self.path_append(dst, directory)

            for file in os.listdir(src):
                shutil.move(self.path_append(src, file), dst)

        path = self.project_path
        path = self.path_append(path, "app")
        path = self.path_append(path, "src")

        if "androidTest" in os.listdir(path):
            move(path, "androidTest")

        if "test" in os.listdir(path):
            move(path, "test")

        if "main" in os.listdir(path):
            move(path, "main")

        self.moved = True


if __name__ == "__main__":
    print(ACCENT_COLOR + WELCOME_TEXT)
    try:
        renamer = AndroidProjectRenamer("/Users/princessyork/Development/Android/AndroidStudioProjects/Test")
        renamer.set_new_package("test.package")
        print(DEFAULT_COLOR + "Old package: " + renamer.old_package)
        print(ACCENT_COLOR + "Will be changed to")
        print(DEFAULT_COLOR + "New package: " + renamer.new_package)
        input(SUCCESS_COLOR + "Press enter to continue...")
        renamer.create_new_package_dirs()
        renamer.update_manifest()
        renamer.move_files()
        renamer.update_files_package()
    except AndroidProjectRenamerException as e:
        print(ERROR_COLOR + e.what)
    except KeyboardInterrupt:
        print()
        print(WARN_COLOR + "Execution is terminated")
