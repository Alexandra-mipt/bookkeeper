"""
tables
"""
from typing import Any
from PyQt6 import QtWidgets

# Создаём класс таблицы отличается тем, что все данные о настройке таблицы вытащим в отдельное
# место, а потом воткнём в приложение.


class BudgetTable(QtWidgets.QTableWidget):
    """Class representing a Budget Table"""
    def __init__(self, rws: int = 3, clmns: int = 3,
                 header_text: str = 'Срок Сумма Бюджет',
                 *args, **kwargs) -> None:
        # Всё лишнее отдаём на откуп исходнику
        super().__init__(*args, *kwargs)
        # число столбцов
        self.setColumnCount(clmns)
        # число строк
        self.setRowCount(rws)
        # Подписываем столбцы
        self.setHorizontalHeaderLabels(header_text.split())
        # настраиваем размеры полей
        for j in range(clmns):
            super().resizeColumnToContents(j)
        self.SetTableData([['День', 'empty', 'empty'],
                           ['Неделя', 'empty', 'empty'],
                           ['Месяц', 'empty', 'empty']])

    # Функция заполнения полей таблицы
    def SetTableData(self, data: list[list[Any]] = None) -> None:
        """Function text is Set Table Data"""
        if data is None:
            data = [['empty' for j in range(self.columnCount())]
                    for j in range(self.rowCount())]

        # Вносим данные
        for j, row in enumerate(data):
            for k, x in enumerate(row):
                self.setItem(j, k, QtWidgets.QTableWidgetItem(x))

        # Делаем красивый вид, настраивая размеры полей
        for j in range(self.columnCount()):
            self.resizeColumnToContents(j)
