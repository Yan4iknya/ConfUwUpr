from os import replace,remove
import os
from zipfile import ZipFile
from application import Application

class Terminal:

    def __init__(self, name, fs_path, file_system: ZipFile):
        self.username = name
        self.fs_path = fs_path
        self.filesystem = file_system
        self.path = ""
        self.application = None

    def link(self, app: Application):
        self.application = app

    def command_dispatcher(self, string):
        line = string.split()
        if line[0] == "exit":
            self.application.exit()
        elif line[0] == "ls":
            self.ls(line[1:])
        elif line[0] == "cd":
            temp_dir = self.cd(line[1:])
            if temp_dir is not None:
                self.path = temp_dir
        elif line[0] == "find":
            self.application.print(self.find(line[1:]),"error")
        elif line[0] == "chown":
            self.application.print(self.chown(line[1:]),"error")
        elif line[0] == "tail":
            self.application.print(self.tail(line[1:]),"error")
        else:
            self.application.print("Работа данной команды не предусмотрена в данном эмуляторе.", "error")

    def ls(self, args):
        work_dir = self.path
        if len(args) > 0:
            work_dir = args[-1]
            work_dir = work_dir.strip('/')
            work_dir = work_dir.split('/')
            new_dir = self.path[:-1].split('/')
            if new_dir == [""]:
                new_dir = []
            for arg in work_dir:
                if arg == "..":
                    if len(new_dir) > 0:
                        new_dir.pop()
                    else:
                        self.application.print("Некорректный путь к директории.", "error")
                        work_dir = ""
                else:
                    new_dir.append(arg)
            new_path = "/".join(new_dir) + "/"
            if new_path == "/":
                work_dir = ""
            for file in self.filesystem.namelist():
                if file.startswith(new_path):
                    work_dir = new_path
            if work_dir is None:
                self.application.print("", "command")
        items = set()
        for item in self.filesystem.namelist():
            if item.startswith(work_dir):
                ls_name = item[len(work_dir):]
                if "/" in ls_name:
                    ls_name = ls_name[:ls_name.index("/")]
                items.add(ls_name)
        self.application.print('\n'.join(sorted(filter(lambda x: len(x) > 0, items))), "command")

    def cd(self, args):
        if len(args) == 0:
            return ""
        directory = args[-1]
        directory = directory.strip('/')
        directory = directory.split('/')
        new_dir = self.path[:-1].split('/')
        if new_dir == [""]:
            new_dir = []
        for arg in directory:
            if arg == "..":
                if len(new_dir) > 0:
                    new_dir.pop()
                else:
                    self.application.print("Некорректный путь к директории.", "error")
                    return
            else:
                new_dir.append(arg)
        new_path = "/".join(new_dir) + "/"
        if new_path == "/":
            return ""
        for file in self.filesystem.namelist():
            if file.startswith(new_path):
                return new_path
        self.application.print("Директория с таким названием отсутствует.", "error")

    def tail(self, params):
        if len(params) == 0:
            return "Неправильное название файла"
        file = params[-1]
        num_lines = 10
        if len(params) > 1 and params[0] == "-n":
            try:
                num_lines = int(params[-2])
            except ValueError:
                return "Некорректное количество строк."

        try:
            with ZipFile(self.fs_path, 'r') as file_system:
                self.filesystem = file_system
                file_path = self.path + file
                if file_path in self.filesystem.namelist():
                    with self.filesystem.open(file_path) as read_file:
                        lines = read_file.read().decode("UTF-8").replace('\r', '').splitlines()
                        tail_lines = '\n'.join(lines[-num_lines:])
                        self.application.print(tail_lines, "command")
                else:
                    self.application.print("Файл не найден в архиве.", "error")
        except Exception as e:
            self.application.print("Ошибка при обработке файла.", "error")
        return ""

    def find(self, args):
        if len(args) < 1:
            return ""
        search_term = args[0]
        results = []
        for item in self.filesystem.namelist():
            if search_term in item:
                results.append(item)
        if results:
            self.application.print('\n'.join(sorted(results)), "command")
            return ""
        else:
            return "Ничего не найдено."

    def chown(self, args):
        if len(args) < 2:
            return "Необходимо указать нового владельца и имя файла."

        new_owner = args[0]
        file_name = args[1]
        file_path = self.path + file_name
        temp_zip_path = self.fs_path + '.tmp'
        self.application.print(f"Владелец файла '{file_name}' изменён на '{new_owner}'.", "command")
        try:
            with ZipFile(self.fs_path, 'r') as zip_file, ZipFile(temp_zip_path, 'w') as temp_zip:
                for item in zip_file.infolist():
                    data = zip_file.read(item.filename)
                    if item.filename == file_path:
                        item.comment = f'owner: {new_owner}'.encode('utf-8')
                    temp_zip.writestr(item, data)
            if os.path.exists(self.fs_path):
                os.remove(self.fs_path)
            replace(temp_zip_path, self.fs_path)
            self.application.print(f"Владелец файла '{file_name}' изменён на '{new_owner}'.", "command")
        except Exception as e:
            self.application.print(f"Ошибка при изменении владельца файла: {e}", "error")
        finally:
            if os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                    return ""
                except Exception:
                    return ""
