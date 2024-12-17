from types import NoneType

import pytest
from zipfile import ZipFile
from terminal import Terminal
from application import Application

@pytest.fixture
def terminal():
    name = "user"
    fs_path = "vfs.zip"
    t = Terminal(name, fs_path, ZipFile(fs_path, "a"))
    return t


def test_init_1(terminal):
    assert terminal.application is None


def test_init_2(terminal):
    assert terminal.filesystem is not None


def test_link(terminal):
    terminal.link(Application(terminal))
    assert terminal.application is not None


def test_cd_1(terminal):
    assert terminal.cd([]) == ""


def test_cd_2(terminal):
    assert terminal.cd(["dir_1/.."]) == ""


def test_ls_1(terminal):
    assert NoneType


def test_ls_2(terminal):
    terminal.path = terminal.cd(["dir_1"])
    assert NoneType


def test_chown_1(terminal):
    assert terminal.chown(["dir_1/dir_1_dir_1/dir_1_dir_1_text_1.txt"]) == "Необходимо указать нового владельца и имя файла."

def test_chown_2(terminal):
    assert terminal.chown(["user1"]) == "Необходимо указать нового владельца и имя файла."

def test_tail_1(terminal):
    assert terminal.tail([]) == "Неправильное название файла"

def test_tail_2(terminal):
    assert terminal.tail(["-n", "g", "dir_1/dir_1_dir_1/dir_1_dir_1_text_1.txt"]) == "Некорректное количество строк."

def test_find_1(terminal):
    terminal.find([])
    assert terminal.find([]) == ""

def test_find_2(terminal, capfd):
    assert terminal.find(["dir_1_dir_1_text_11.txt"]) == "Ничего не найдено."
