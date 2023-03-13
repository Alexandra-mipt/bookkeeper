"""
sqlite repository
"""
from inspect import get_annotations
import sqlite3
from typing import Any
import os.path
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def ecran(value: str | Any) -> str | Any:
    """Function ecran"""
    if isinstance(value, str):
        return f'\'{value}\''
    return value


class SQLiteRepository(AbstractRepository[T]):
    """Class representing a SQLiteRepository"""
    def __init__(self, db_file: str, cls: type) -> None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_file)
        # Нужно сохранить исходный тип классов, которые потом будем принимать
        self.ini_class_type = cls
        self.db_file = db_path
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        # Нужно удалить pk, чтобы он не мешался, так как это индекс иной БД
        self.fields.pop('pk')
        names = ', '.join(self.fields.keys())
        print(f'Поля в БД: {names}')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                  f'(CONSTRAINT idx INTEGER PRIMARY KEY, {names})')
            cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                        f'(idx INTEGER PRIMARY KEY, {names})')
            con.commit()

    def obertka(self, objbad: Any) -> list[type] | None:
        """Function obertka"""
        if len(objbad) == 0:
            return None
        elif len(objbad) == 1:
            objbad = objbad[0]
            objgood = self.ini_class_type()
            # Достаём имена всех кусочков класса
            temp_name = get_annotations(self.ini_class_type, eval_str=True)
            names = tuple(temp_name.keys())
            for j in range(len(names)-1):
                setattr(objgood, names[j], objbad[j+1])
                setattr(objgood, 'pk', objbad[0])
            print(f'Сформирован: {str(objgood)}')
            return [objgood]
        else:
            temp_name = get_annotations(self.ini_class_type, eval_str=True)
            names = tuple(temp_name.keys())
            arr: list[type] = []
            for k in range(len(objbad)):
                objbad_temp = objbad[k]
                objgood = self.ini_class_type()
                for j in range(len(names) - 1):
                    setattr(objgood, names[j], objbad_temp[j + 1])
                setattr(objgood, 'pk', objbad_temp[0])
                arr = arr + [objgood]
            print(f'Сформированы: {str(arr)}')
            return arr

    def add(self, obj: T) -> int:
        # Для начала проверка, что мы добавляем объект, который ещё не содержит ключа
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled \'pk\' attribute')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values)
            cur.execute(f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values)
            obj.pk = cur.lastrowid
            con.commit()
        print(f'Создан объект: {str(self.get(obj.pk))}')
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'SELECT * FROM {self.table_name} WHERE (idx = {pk})')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE (idx = {pk})')
            obj = cur.fetchall()
            # Закрываем БД
            con.commit()
        print(f'Получен объект {obj}')
        return self.obertka(obj)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

        # Если условие не задано, то вернуть должны всё
        if where is None:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                print(f'SELECT * FROM {self.table_name}')
                cur.execute(f'SELECT * FROM {self.table_name}')
                obj = cur.fetchall()
                con.commit()

        else:
            # Вытащим имена колонок, по которым идёт сортировка
            names_of_columns = where.keys()
            conditions = [f'{name} {where.get(name)}' for name in names_of_columns]
            conditions = tuple(conditions)
            temp_cond = ' AND '.join(conditions)

            # Открываем БД
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                print(f'SELECT * FROM {self.table_name} WHERE ({temp_cond})')
                cur.execute(f'SELECT * FROM {self.table_name} WHERE ({temp_cond})')
                obj = cur.fetchall()
                con.commit()

        print(f'Получены объекты {obj}')
        return self.obertka(obj)

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        pk = obj.pk
        if self.get(pk) is None:
            raise ValueError(f'No object with idx = {obj.pk} in DB.')

        # Вытащили новую информацию
        names = tuple(self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        update_data = [f'{names[j]} = ?' for j in range(len(self.fields))]
        update_data = tuple(update_data)
        # соорудим часть запроса
        update_zapros = ', '.join(update_data)

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'UPDATE {self.table_name} '
                  f'SET {update_zapros} WHERE (idx = {pk})', values)
            cur.execute(f'UPDATE {self.table_name} '
                        f'SET {update_zapros} WHERE (idx = {pk})', values)
            con.commit()
        print(f'Обновление объекта произведено. Текущие параметры {self.get(pk)}')

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        if self.get(pk) is None:
            raise KeyError(f'No object with idx = {pk} in DB.')

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'DELETE FROM {self.table_name} WHERE (idx = {pk})')
            cur.execute(f'DELETE FROM {self.table_name} WHERE (idx = {pk})')
            con.commit()

        print('Запись удалена')

    def delete_all(self) -> None:
        """Function delete_all"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            print(f'DELETE FROM {self.table_name}')
            cur.execute(f'DELETE FROM {self.table_name}')
            con.commit()
        print('Все записи удалены')
