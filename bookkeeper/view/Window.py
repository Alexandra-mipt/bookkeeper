"""
window
"""
import os
from PyQt6 import QtWidgets, QtGui
# from typing import Any
from bookkeeper.view.ExpensesTable import ExpenseTable
from bookkeeper.view.BudgetTable import BudgetTable
# from bookkeeper.view.EasyComboBox import EasyComboBox
from bookkeeper.view.DeleteLine import DeleteLine
from bookkeeper.view.ExpAddCompany import ExpAddCompany
from bookkeeper.models.category import Category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Start_pic_path = os.path.join(BASE_DIR, 'Money.jpg')

# Создаём класс окна, в котором опишем основную начинку


class BookkeeperWindow(QtWidgets.QWidget):
    """Class representing a Bookkeeper Window"""
    def __init__(self, ctg: list[Category] = [Category('Empty')],
                 expenses_adder=None,
                 expenses_updater=None,
                 expenses_deleter=None,
                 ctg_pk_2_name=None,
                 category_adder=None,
                 category_updater=None,
                 category_deleter=None,
                 budget_updater=None,
                 *args, **kwargs):
        # Так как переопределяем init, то сначала
        # надо передать все системные аргументы туда, где они нужны
        super().__init__(*args, **kwargs)

        # Опишем элементы окна сверху вниз, слева-направо
        # Подпись у таблички
        self.TableLabel = self.MakeLabel('Таблица последних расходов')

        # Поле для удаления расхода
        self.DeleteLine = DeleteLine(expenses_deleter)
        self.DeleteLine.setMaximumWidth(300)
        # Таблица расходов
        # Вариант с созданием отдельного класса таблицы
        self.ExpensesTable = ExpenseTable(expenses_updater, ctg_pk_2_name)

        # Подпись к таблице с бюджетом
        self.BudgetLabel = self.MakeLabel('Бюджет')

        # Таблица бюджета
        self.BudgetTable = BudgetTable(budget_updater)

        # Кусок с вводом данных расхода и редактурой категории
        self.ExpenseAndCategoryEdit = ExpAddCompany(ctg, expenses_adder, category_adder,
                                                    category_updater, category_deleter)

        # Строим раскладку:
        # Имя таблицы и поле для удаления соберём вместе
        horiz0 = QtWidgets.QHBoxLayout()
        # Подпись таблицы
        horiz0.addWidget(self.TableLabel)
        # Строка для удаления расходов
        horiz0.addWidget(self.DeleteLine)

        # Разложим сюда то, что раскладывается просто сверху вниз
        vert1 = QtWidgets.QVBoxLayout()
        # Нулевой горизонтальный блок, что описан выше
        vert1.addLayout(horiz0)
        # Таблицу расходов
        vert1.addWidget(self.ExpensesTable)
        # Подпись бюджета
        vert1.addWidget(self.BudgetLabel)
        # Таблицу бюджета
        vert1.addWidget(self.BudgetTable)
        # Кусок изменения всего
        vert1.addWidget(self.ExpenseAndCategoryEdit)

        # Дополнительно создадим поле для картиночки
        self.PicField1 = QtWidgets.QLabel()
       # self.pixmap1 = QtGui.QPixmap('Money.jpg')
       # print(self.pixmap1.isNull())
       # self.PicField1.setPixmap(self.pixmap1)
        self.PicField1.setScaledContents(True)
        self.PicField1.setMaximumWidth(350)
        self.PicField1.setMaximumHeight(300)

        # поле для картинки
        self.PicField2 = QtWidgets.QLabel()
        self.pixmap2 = QtGui.QPixmap('Dog.jpg')
        print(self.pixmap2.isNull())
        self.PicField2.setPixmap(self.pixmap2)
        self.PicField2.setScaledContents(True)
        self.PicField2.setMaximumWidth(350)
        self.PicField2.setMaximumHeight(300)

        hor = QtWidgets.QHBoxLayout()
        hor.addWidget(self.PicField1)
        hor.addLayout(vert1)
        hor.addWidget(self.PicField2)

        # Присвоим полученную раскладку соотв полю self
        self.layout = hor
        # Применим эту раскладку к окну
        self.setLayout(self.layout)

    # Функция создания подписи у чего-либо
    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """Function text is MakeLabel"""
        # Создаём подпись
        label_obj = QtWidgets.QLabel()
        # Присваиваем ей имя
        label_obj.setText(text)
        return label_obj

    # Функция создания поля с возможностью ввода
    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """Function text is MakeLineEdit"""
        LineEdit_obj = QtWidgets.QLineEdit()
        # фоновую подпись
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    # Функция создания кнопки
    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """Function text is Make Button"""
        # Создали объект кнопки
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj

    # Обработка события начала изменения текста - ожидаем обработки окончания ввода
    def text_is_changing(self):
        """Function text is text is changing"""
        # подключаем после окончания обработки редактирования - обработку результата
        self.editingFinished.connect(self.get_amount)

    # Обрабатывается окончание редактирования - получаем расход
    def get_amount(self):
        """Function text is get amount"""
        # Отключили отслеживание редактирования
        self.editingFinished.disconnect()
        # Получили введённый текст
        amount = self.displayText()
        # Проверили, что число
        try:
            amount = float(amount)
        except amount.DoesNotExist:
            raise ValueError('Некорректный ввод!')
        # Очистили поле редактирования
        self.clear()
        print(str(amount))
