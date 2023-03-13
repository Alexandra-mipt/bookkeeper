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
    # SQLite для запросов требует, чтобы у строк были одинарные кавычки
    # но просто так их не передать, поэтому их ЭКРАНируем: \' .
    # Для унификации через экран прогоняются все числа.
    # Те, которые требуют экранирования, его получают.
    # Которые не требуют - возвращаются.
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

    # sqlite возвращает запросы в виде листа кортежей.
    # Т.е. одна строка - один кортеж.
    # Но на вход подаются данные в виде какого-то класса.
    # Чтобы вход и выход можно было сверять, необходимо
    # Оформлять возврат в виде того же класса.
    # Для этого и служит следующая функция
    def obertka(self, objbad: Any) -> list[type] | None:
        """Function obertka"""
        # Если только одна запись - вернём всё равно list из одного объекта
        if len(objbad) == 0:
            return None
        elif len(objbad) == 1:
            objbad = objbad[0]
            # Создаём пустой объект нужного класса
            objgood = self.ini_class_type()
            # Достаём имена всех кусочков класса
            temp_name = get_annotations(self.ini_class_type, eval_str=True)
            names = tuple(temp_name.keys())
            # Оборачиваем всё из вывода sql в старый класс
            # -1, так как среди имён в конце есть pk
            for j in range(len(names)-1):
                setattr(objgood, names[j], objbad[j+1])
                setattr(objgood, 'pk', objbad[0])
            print(f'Сформирован: {str(objgood)}')
            return [objgood]
        else:
            # Достаём имена всех кусочков класса
            temp_name = get_annotations(self.ini_class_type, eval_str=True)
            names = tuple(temp_name.keys())
            # Заранее создаём список вывода
            arr: list[type] = []
            for k in range(len(objbad)):
                # Выделили из списка кортеж
                objbad_temp = objbad[k]
                # Создаём пустой объект нужного класса
                objgood = self.ini_class_type()
                # Оборачиваем всё из вывода sql в старый класс
                for j in range(len(names) - 1):
                    setattr(objgood, names[j], objbad_temp[j + 1])
                setattr(objgood, 'pk', objbad_temp[0])
                # Добавляем результат в список вывода
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
        # Открыли базу данных как con
        with sqlite3.connect(self.db_file) as con:
            # Что-то сделали с базой данных, чтобы из этого
            # чего-то работать с БД
            cur = con.cursor()
            # неизвестная штука
            cur.execute('PRAGMA foreign_keys = ON')
            # Передаём запрос в SQL формате на выдачу всех пунктов записи
            # из иаблицы table_name по условию, что ключ есть pk
            print(f'SELECT * FROM {self.table_name} WHERE (idx = {pk})')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE (idx = {pk})')
            # Вытягиваем полученный ответ в объект
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
            # Открываем БД
            with sqlite3.connect(self.db_file) as con:
                # Что-то сделали с базой данных, чтобы из этого
                # чего-то работать с БД
                cur = con.cursor()
                # Нечто
                cur.execute('PRAGMA foreign_keys = ON')
                # Передаём запрос в SQL формате на выдачу всех пунктов записи
                # из иаблицы table_name по условию, что столбцы names_of_columns
                # удовлетворяют значениям из values
                print(f'SELECT * FROM {self.table_name}')
                cur.execute(f'SELECT * FROM {self.table_name}')
                # Вытягиваем полученный ответ в объект
                obj = cur.fetchall()
                con.commit()

        # Если условие задано, то вернуть должны по условию
        else:
            # Вытащим имена колонок, по которым идёт сортировка
            names_of_columns = where.keys()
            # Формируем значения условий
            conditions = [f'{name} {where.get(name)}' for name in names_of_columns]
            conditions = tuple(conditions)
            # Теперь надо соорудить часть запроса, так как нельзя параметризацией
            # передавать имя таблицы и её столбцов.
            # условие задаётся в форме словаря, то не
            # подразумевает записи в услвовие свойства OR или AND.
            # Поэтому объединяем по принципу AND
            temp_cond = ' AND '.join(conditions)

            # Открываем БД
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                # Передаём запрос в SQL формате на выдачу всех пунктов записи
                # из таблицы table_name по условию, что столбцы names_of_columns
                # удовлетворяют значениям из values
                print(f'SELECT * FROM {self.table_name} WHERE ({temp_cond})')
                cur.execute(f'SELECT * FROM {self.table_name} WHERE ({temp_cond})')
                # Вытягиваем полученный ответ в объект
                obj = cur.fetchall()
                con.commit()

        print(f'Получены объекты {obj}')
        return self.obertka(obj)

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        # Вытащили, какой именно объект обновляем
        pk = obj.pk
        # Проверили, что объект есть
        if self.get(pk) is None:
            raise ValueError(f'No object with idx = {obj.pk} in DB.')

        # Вытащили новую информацию
        names = tuple(self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        update_data = [f'{names[j]} = ?' for j in range(len(self.fields))]
        update_data = tuple(update_data)
        # соорудим часть запроса, так как нельзя параметризацией
        update_zapros = ', '.join(update_data)

        # Открыли базу данных как con
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            # Передаём запрос в SQL формате на UPDATE всех строк
            # с ключом pk
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

        # Открыли базу данных как con
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
