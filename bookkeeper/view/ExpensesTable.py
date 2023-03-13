"""
add expenses table
"""
# import sys
from PyQt6 import QtWidgets
from bookkeeper.models.expense import Expense


class ExpenseTable(QtWidgets.QTableWidget):
    """Class representing a ExpenseTable"""
    def __init__(self,
                 expenses_updater=None,
                 ctg_pk_2_name=None,
                 rws: int = 50,
                 clmns: int = 5,
                 header_text: str = 'Дата Сумма Категория Комментарий Ключик',
                 *args, **kwargs) -> None:

        super().__init__(*args, *kwargs)

        self.expenses_updater = expenses_updater
        self.ctg_pk_2_name = ctg_pk_2_name

        self.setColumnCount(clmns)
        self.setRowCount(rws)
        self.setHorizontalHeaderLabels(header_text.split())
        # Делаем красивый вид, настраивая размеры полей.
        for j in range(clmns):
            self.resizeColumnToContents(j)
        # Заполняем таблицу пустотой
        self.SetTableData()

        self.expenses_attrs = {0: 'expense_date', 1: 'amount',
                               2: 'category', 3: 'comment', 4: 'pk'}

        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        self.cellDoubleClicked.connect(self.cell_double_clicked)

    # Функция заполнения полей таблицы
    def SetTableData(self, data: list[list[str]] = None) -> None:
        """Function text is Set Table Data"""
        if data is None:
            data = [['empty' for j in range(self.columnCount())]
                    for j in range(self.rowCount())]

        self.data = data

        # Вносим данные
        for j, row in enumerate(data):
            for k, x in enumerate(row):
                self.setItem(j, k, QtWidgets.QTableWidgetItem(x))

        # Делаем красивый вид, настраивая размеры полей.
        for j in range(self.columnCount()):
            self.resizeColumnToContents(j)

    # Обработка события двойного щелчка - ожидаем обработки редактирования
    def cell_double_clicked(self) -> None:
        """Function text is cell double clicked"""
        print('Ожидаем конца редактирования')
        self.cellChanged.connect(self.cell_changed)

    # Обрабатывается окончание редактирования - составляем новые параметры записи
    def cell_changed(self, row, column) -> None:
        """Function text is cell changed"""
        print('Приступили к обработке события после конца редактирования')
        self.cellChanged.disconnect(self.cell_changed)
        print('Отключили кнопку, чтобы не было дублирования')
        pk = self.data[row][-1]
        print('Определили ключ записи')
        # Новые параметры затраты
        new_val = self.item(row, column).text()
        print('Определили новые параметры затраты')
        attr = self.expenses_attrs[column]
        print('Вернули имя атрибута, которому меняли значение')
        print('Передаём данные в обработчик обновлений затрат')
        self.expenses_updater(pk, [attr], [new_val])

    # Запись в таблицу расходов из БД
    def set_expenses(self, expenses: list[Expense]) -> None:
        """Function text is set expenses"""
        # Сохраним в нашем классе расходы
        self.expenses = expenses
        # Переведём данные из формата Expenses в строки
        self.data = self.expenses_to_data(self.expenses)
        self.clearContents()
        self.SetTableData(self.data)

    # Конвертер из типов характерных для Expenses в строки
    def expenses_to_data(self, expenses: list[Expense] | None) -> list[list[str]]:
        """Function text is expenses to data"""
        # Лист для ответов
        data = []
        # Проверим, что записи вообще есть:
        if expenses is None:
            data = [['Empty', 'Empty', 'Empty', 'Empty', 'Empty']]
        else:
            # Прогоним каждый расход
            for expense in expenses:
                # Разложим трату на лист из строк
                item = [str(expense.expense_date),
                        str(expense.amount),
                        str(self.ctg_pk_2_name(expense.category)),
                        str(expense.comment),
                        str(expense.pk)]
                data.append(item)
        return data
