from sys import argv
from zipfile import ZipFile
from application import Application
from terminal import Terminal
import csv

def main():
    if len(argv) > 1:
        config_file = argv[1]
        try:
            with open(config_file, "r", encoding="UTF-8") as file:
                reader = csv.DictReader(file)
                for row in reader:  # Считываем каждую строку как словарь
                    if "username" in row and "filesystem_path" in row:
                        username = row["username"]
                        filesystem_path = row["filesystem_path"]
                        with ZipFile(filesystem_path, 'a') as file_system:
                            Application(Terminal(username, filesystem_path, file_system)).run()
                    else:
                        print("Отсутствуют необходимые данные в конфигурации.")
                    break  # Обрабатываем только первую строку
        except FileNotFoundError:
            print(f"Файл {config_file} не найден.")
    else:
        print("Аргументы не были переданы.")

if __name__ == "__main__":
    main()
