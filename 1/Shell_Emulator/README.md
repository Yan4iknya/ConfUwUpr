# **Задание №1**
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата **zip**. Эмулятор должен работать в режиме **GUI**.

Конфигурационный файл имеет формат **csv** и содержит:
- Имя пользователя для показа в приглашении к вводу.
- Путь к архиву виртуальной файловой системы.
- Путь к стартовому архиву

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
1. find.
2. chown.
3. tail.

Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 2 теста.
# Установка
Перед началом работы с программой требуется скачать репозиторий и необходимую библиотеку для тестов. Для этого можно воспользоваться командами ниже.
```Bash
git clone https://github.com/Yan4ikNya/1/Shell_Emulator
```
```Bash
pip install -U pytest
```
# Запуск
Перед запуском необходимо клонировать репозиторий в среду разработки.

Обязательно прописать путь к файловой системе в config.csv.

Запуск main.py:
```Bash
py main.py config.csv 
```
Запуск тестов
```Bash
pytest -v test.py
```
# Команды
В квадратных скобках опциональные настройки команд.

``` ls <path> ``` - Список файлов и директорий

``` cd <path> ``` - Смена директории

``` exit ``` - Выход из эмулятора

``` tail [-n int] <path> ``` - Создание файла

``` chown <user> <path> ``` - Вывод содержимого файла

``` find <name> ``` - Вывод содержимого файла

# Тесты
## ls
![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/ls.PNG)
## cd
![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/cd.PNG)
## tail
![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/tail.PNG)
## chown
![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/chown.PNG)
## find
![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/find.PNG)
## Общие тесты через pytest
![]![](https://github.com/Yan4iknya/ConfUwUpr/blob/main/1/Shell_Emulator/test.PNG)
