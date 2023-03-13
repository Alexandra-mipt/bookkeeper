"""
add company
"""
from PyQt6 import QtWidgets
from bookkeeper.models.category import Category
from bookkeeper.view.EasyComboBox import EasyComboBox
from bookkeeper.view.CtgWorkWindow import CategoryAUDWindow

# Группа виджетов, в которой можно добавлять расходы


class ExpAddCompany(QtWidgets.QGroupBox):
    """Class representing a ExpAddCompany"""
    def __init__(self,
                 ctg: list[Category] = None,
                 expense_adder=None,
                 ctg_adder=None,
                 ctg_updater=None,
                 ctg_deleter=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expense_adder = expense_adder
        # Сохранили в классе функции добавления, удаления и обновления категории
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter

        self.ExpenseLabel = self.MakeLabel('Сумма')
        self.ExpenseField = self.MakeLineEdit('Введи сумму')

        self.CategoryLabel = self.MakeLabel('Категория')
        self.CategoryLabel.setMaximumWidth(60)
        # Поле для выбора категории
        self.CategoryBox = EasyComboBox()
        self.CategoryBox.setMaximumWidth(1200)
        self.CategoryEditButton = self.MakeButton('Редактировать категории')
        # Подгоним размер
        self.CategoryEditButton.setMaximumWidth(200)

        # Подпись для поля с введением комментария
        self.CommLabel = self.MakeLabel('Комментарий')
        self.CommField = self.MakeLineEdit('Введи комментарий (опционально)')

        # Кнопка для подтверждения
        self.ExpenseAccept = self.MakeButton('Добавить расход')

        horiz1 = QtWidgets.QHBoxLayout()
        # Подпись к полю
        horiz1.addWidget(self.ExpenseLabel)
        horiz1.addWidget(self.ExpenseField)

        # Создадим общую вертикальную раскладку
        vert1 = QtWidgets.QVBoxLayout()
        vert1.addLayout(horiz1)

        horiz2 = QtWidgets.QHBoxLayout()
        horiz2.addWidget(self.CategoryLabel)
        # Выпадающее меню категорий
        horiz2.addWidget(self.CategoryBox)
        horiz2.addWidget(self.CategoryEditButton)

        # Добавим эту горизонтальную раскладку следующей строкой в вертикальную
        vert1.addLayout(horiz2)

        horiz3 = QtWidgets.QHBoxLayout()
        horiz3.addWidget(self.CommLabel)
        horiz3.addWidget(self.CommField)

        vert1.addLayout(horiz3)
        vert1.addWidget(self.ExpenseAccept)

        self.setLayout(vert1)

        self.ExpenseAccept.clicked.connect(self.add_expense)
        self.CategoryEditButton.clicked.connect(self.ctg_edit_show_window)

        self.set_categories(ctg)

    # Установка категорий: их добавление в выпадающее меню
    def set_categories(self, ctg: list[Category] | None) -> None:
        """Function text is set categories"""
        self.categories = ctg
        # Проверим, что категории вообще есть
        if ctg is None:
            self.CategoryBox.set_items(['Empty'])
        else:
            # Получим имена категорий
            self.ctg_names = [category.name for category in ctg]
            print(f'Получены имена {self.ctg_names}')
            # Установим категории в выпадающее меню
            self.CategoryBox.set_items(self.ctg_names)

    # Опишем процедуру добавления расхода
    def add_expense(self):
        """Function text is add expense"""
        print('Приняты данные на добавление')
        amount = self.ExpenseField.text()
        print('Считано число')
        category = self.CategoryBox.currentText()
        print('Считана категория')
        comm = self.CommField.text()
        print('Считан комментарий')
        print('Передаём данные в создатель')
        self.expense_adder(amount, category, comm)
        self.ExpenseField.clear()
        self.CategoryBox.clear()
        self.CommField.clear()

    def ctg_edit_show_window(self):
        """Function text is ctg edit show window"""
        # Запускаем окошко, делая его объектом класса, что создан выше
        self.window2 = CategoryAUDWindow(self.ctg_adder,
                                         self.ctg_updater, self.ctg_deleter)
        self.window2.setWindowTitle('Изменение категорий')
        self.window2.resize(300, 600)
        self.window2.show()

    # Функция создания подписи у чего-либо
    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """Function text is Make Label"""
        label_obj = QtWidgets.QLabel()
        label_obj.setText(text)
        return label_obj

    # Функция создания поля с возможностью ввода
    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """Function text is Make Line Edit"""
        # Создаём строку объект строки ввода
        LineEdit_obj = QtWidgets.QLineEdit()
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    # Функция создания кнопки
    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """Function text is Make Button"""
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
