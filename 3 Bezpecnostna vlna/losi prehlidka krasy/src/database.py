import os

from typing import Optional, List, Any
from threading import Lock
from os import path
from json import loads, dumps
from lzma import open


class Table:
    def __init__(self, name: str, database: "Database") -> None:
        self.__database = database
        self.__name = name

    def set_key(self, key: str, value: Optional[str]) -> None:
        self.__database.set_key(self, key, value)

    def get_key(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.__database.get_key(self, key, default)

    def set_key_object(self, key: str, value: Any) -> None:
        self.set_key(key, dumps(value))

    def get_key_object(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        text = self.get_key(key)
        if text is None:
            return default
        return loads(text)

    def __getitem__(self, item: str) -> Optional[str]:
        # this allow us to call Table[item]
        return self.get_key_object(item)

    def __setitem__(self, key: str, value: Any) -> None:
        # this allow us to call Table[item] = value
        self.set_key_object(key, value)

    def __delitem__(self, key: str) -> None:
        # this allow us to call del Table[item]
        self.set_key_object(key, None)

    @property
    def name(self) -> str:
        return self.__name


class Database:
    def __init__(self, file: str) -> None:
        self.__file = file
        self.__file_lock = Lock()

    def open_table(self, name: str) -> Table:
        return Table(name, self)

    def get_key(self, table: Table, key: str, default: Optional[str] = None) -> Optional[str]:
        table_line = self.__get_table_line_content(table)
        if table_line is None:
            return default

        for item in table_line.split('|'):
            if item.startswith(key + ':::'):
                return item[len(key) + 3:]

        return default

    def set_key(self, table: Table, key: str, value: Optional[str]) -> None:
        # this forces that only one process can read/write to file at once
        with self.__file_lock:
            if path.exists(self.__file):
                with open(self.__file, 'rb') as f:
                    lines = f.read().decode('utf8').splitlines()
            else:
                lines = []

            line_content = self.__get_table_line_content(table, lines)
            other_lines = [line for line in lines if not line.startswith(table.name + '|')]

            if line_content is None:
                other_items = []
            else:
                other_items = [item for item in line_content.split('|') if not item.startswith(key + ':::')]

            items = list(other_items)
            if value is not None:
                items += [key + ':::' + value]

            lines = list(other_lines)
            if len(items) > 0:
                lines += ['|'.join([table.name] + items)]

            # create parent directory if does not exist yet
            os.makedirs(path.realpath(path.join(self.__file, path.pardir)), exist_ok=True)

            with open(self.__file, 'wb') as f:
                f.write('\n'.join(lines).encode('utf8'))

    def __get_table_line_content(self, table: Table, lines: Optional[List[str]] = None) -> Optional[str]:
        if not path.exists(self.__file):
            return None

        if lines is None:
            # this forces that only one process can read/write to file at once
            with self.__file_lock:
                with open(self.__file, 'rb') as f:
                    lines = f.read().decode('utf8').splitlines()

        for line in lines:
            if line.startswith(table.name + '|'):
                return line[len(table.name) + 1:]

        return None
