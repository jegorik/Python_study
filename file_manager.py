import os
import sys
import shutil
from pathlib import Path

"""Defines a class for handling error messages related to file management operations."""


class Errors:
    def __init__(self):
        """Dictionary mapping command names to specific error messages."""
        self.errors = {
            'wrong_arguments': {
                'cd': 'Invalid directory',
                'cp': 'Specify the file',
                'rm': 'Specify the file or directory',
                'mv': 'Specify the current name of the file or directory and the new location and/or name',
                'mkdir': 'Specify the name of the directory to be made',
            },

            'os_errors': {
                'WrongCommandError': 'Invalid command',
                'DirectoryNotFoundError': 'Invalid directory',
                'InvalidParameterError': 'Invalid parameter',
                FileNotFoundError: 'No such file or directory',
                PermissionError: 'Permission denied',
                FileExistsError: 'The directory already exists',
                TypeError: 'Specify the current name of the file or directory and the new location and/or name'
            }
        }

    def __call__(self, command):
        """Callable method that returns an error description based on the command."""
        return self._get_error_description(command)

    def _get_error_description(self, command):
        """Private method that retrieves an error message based on the command from the wrong_arguments dictionary."""
        return self.errors.get(command)


"""Defines a class representing a command with associated functionality and argument requirements."""


class Command:
    def __init__(self, func, num_args, exist):
        self.func = func  # The function to execute for this command.
        self.num_args = num_args  # The number of arguments this command expects.
        self.multiarg = exist  # Boolean indicating if the command can accept multiple arguments.

    def __call__(self, *args, **kwargs):
        """Callable method that executes the command's function with the provided arguments."""
        return self.func(*args, **kwargs)


"""Defines a class for a simple file manager that supports basic file and directory operations."""


class FileManager:
    def __init__(self):
        """Initializes the file manager with the current directory and available commands."""
        self._current_dir = Path.cwd()  # Sets the initial directory to the current working directory.
        """Dictionary mapping command names to Command objects, specifying the function, argument count,
        and multi-argument support."""
        self._commands = {
            'pwd': Command(self._pwd, 0, False),
            'cd': Command(self._cd, 1, False),
            'cp': Command(self._cp, 2, False),
            'ls': Command(self._ls, 0, True),
            'rm': Command(self._rm, 1, False),
            'mv': Command(self._mv, 2, False),
            'mkdir': Command(self._mkdir, 1, False),
            'quit': Command(self._quit, 0, False)
        }
        self.errors = Errors().errors  # Creates an instance of the Errors class for error handling.

    def _pwd(self):
        """Method to return the current working directory."""
        return self._current_dir

    def _cp(self, file, new_file):
        """Copy a file or all files with a given extension to a new location."""
        if file.startswith('.'):
            return self._copy_files_with_extension(file, new_file)
        else:
            return self._move_copy_file(file, new_file, 'cp')

    def _mv(self, file_name, new_path):
        """Move a file or all files with a given extension to a new location."""
        if file_name.startswith('.'):
            return self._move_files_with_extension(file_name, new_path)
        else:
            return self._move_copy_file(file_name, new_path, 'mv')

    def _move_copy_file(self, file, new_file, action):
        local_file = self._current_dir / file
        dest_file = Path(new_file) if Path(new_file).is_absolute() else self._current_dir / new_file
        if dest_file.is_dir():
            dest_file = dest_file / file
        if dest_file.exists():
            if action == 'mv':
                return 'The file or directory already exists'
            elif action == 'cp':
                user_input = input(f'{file} already exists in this directory. Replace? (y/n): ')
                if user_input.lower() != 'y':
                    return
        try:
            if action == 'mv':
                shutil.move(local_file, dest_file)
            elif action == 'cp':
                shutil.copy2(local_file, dest_file)
        except FileNotFoundError as e:
            return self.errors['os_errors'].get(type(e))
        return f'{file} {"moved" if action == "mv" else "copied"} successfully.'

    def _copy_files_with_extension(self, extension, target_dir):
        files_copied = self._process_files_with_extension(extension, target_dir, 'cp')
        if not files_copied:
            return f"File extension {extension} not found in this directory."

    def _move_files_with_extension(self, extension, target_dir):
        files_moved = self._process_files_with_extension(extension, target_dir, 'mv')
        if not files_moved:
            return f"File extension {extension} not found in this directory."

    def _process_files_with_extension(self, extension, target_dir, action):
        files = list(self._current_dir.glob(f'*{extension}'))
        if not files:
            return False
        for file in files:
            new_file_path = Path(target_dir) / file.name
            if new_file_path.exists():
                user_input = input(f'{file.name} already exists in this directory. Replace? (y/n): ')
                while user_input.lower() not in ['y', 'n']:
                    user_input = input('Invalid input. Please enter "y" or "n": ')
                if user_input.lower() == 'n':
                    continue
            if action == 'cp':
                shutil.copy2(file, new_file_path)
            elif action == 'mv':
                shutil.move(file, new_file_path)
        return True

    def _cd(self, target_dir):
        """Method to change the current directory."""
        try:
            new_dir = self._current_dir / target_dir
            new_dir.resolve(strict=True)
            os.chdir(new_dir)
            self._current_dir = new_dir
            print(self._current_dir)
        except FileNotFoundError:
            return self.errors['os_errors'].get('DirectoryNotFoundError')

    def _ls(self, parameter=None):
        """Method to list the contents of the current directory or a specified directory."""
        available_params = ('-l', '-lh')
        if parameter in available_params or parameter is None:
            dir_content = self._dir_content(parameter)
            return '\n'.join(str(i) for i in dir_content)
        else:
            return self.errors['os_errors'].get('InvalidParameterError')

    def _dir_content(self, show_details=None):
        """Helper method to retrieve directory contents based on detail level."""
        dirs, files = [], []
        for entry in os.scandir():
            if entry.is_dir():
                dirs.append(entry.name)
            else:
                if show_details == '-l':
                    files.append(f'{entry.name} {entry.stat().st_size}')
                elif show_details == '-lh':
                    files.append(f'{entry.name} {self._human_readable_size(entry.stat().st_size)}')
                else:
                    files.append(entry.name)
        dirs.sort()
        files.sort()
        return dirs + files

    def _human_readable_size(self, file_size):
        """Converts file size to a human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if file_size < 1024.0 or unit == 'PB':
                break
            file_size /= 1024.0
        return f"{file_size:.0f}{unit}"

    def _rm(self, target):
        """Remove a file or directory based on the target parameter.

        If the target starts with '.', it treats it as an extension and removes all files with that extension in the current directory.
        Otherwise, it treats the target as a filename or directory name and attempts to remove it.
        """
        try:
            if target.startswith('.'):
                return self._remove_files_by_extension(target)
            else:
                return self._remove_target(target)
        except (FileNotFoundError, PermissionError) as e:
            return self.errors['os_errors'].get(type(e))
        except Exception as e:
            return f"Error removing '{target}': {e}"

    def _remove_files_by_extension(self, extension):
        """Remove all files in the current directory with the given extension."""
        files_removed = False  # Flag to track if any files were removed
        for file in self._current_dir.iterdir():
            if file.is_file() and file.name.endswith(extension):
                file.unlink()
                files_removed = True  # Set the flag to True if a file is removed
        if not files_removed:
            return f"File extension {extension} not found in this directory."

    def _remove_target(self, target):
        """Remove a specific file or directory."""
        target_path = self._current_dir / target
        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()

    def _mkdir(self, dir_name):
        """Method to create a new directory."""
        try:
            (self._current_dir / dir_name).mkdir()
        except FileExistsError:
            return self.errors['os_errors'].get(FileExistsError)

    def _quit(self):
        """Method to exit the file manager."""
        sys.exit()

    def run(self):
        """Main loop to run the file manager, accepting and executing commands."""
        print('Input the command:')
        while True:
            user_input = input().split()
            if not user_input:
                print('Input command')
            else:
                command_name, *args = user_input
                command = self._commands.get(command_name)
                if command:
                    if len(args) >= command.num_args or command.multiarg:
                        try:
                            result = command(*args)
                            if result:
                                print(result)
                        except TypeError:
                            print(self.errors['os_errors'].get(TypeError))
                    else:
                        print(self.errors['wrong_arguments'].get(command_name))
                else:
                    print(self.errors['os_errors'].get('WrongCommandError'))


def main():
    """Main function to run the file manager."""
    file_manager = FileManager()
    file_manager.run()


if __name__ == '__main__':
    main()
