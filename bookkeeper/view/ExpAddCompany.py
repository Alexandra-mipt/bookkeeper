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
        # Всё остальное на родителя
        super().__init__(*args, **kwargs)
        # Записали функцию добвления расхода
        self.expense_adder = expense_adder
        # Сохранили в классе функции добавления, удаления и обновления категории
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter

        # Подпись для поля с введением суммы расхода
        self.ExpenseLabel = self.MakeLabel('Сумма')
        # Поле для введения суммы расхода
        self.ExpenseField = self.MakeLineEdit('Введи сумму')

        # Подпись к полю выбора категории
        self.CategoryLabel = self.MakeLabel('Категория')
        # Подгоним размер
        self.CategoryLabel.setMaximumWidth(60)
        # Поле для выбора категории
        self.CategoryBox = EasyComboBox()
        # Подгоним размер
        self.CategoryBox.setMaximumWidth(1200)
        # Кнопка для открытия окна редактуры категорий
        self.CategoryEditButton = self.MakeButton('Редактировать категории')
        # Подгоним размер
        self.CategoryEditButton.setMaximumWidth(200)

        # Подпись для поля с введением комментария
        self.CommLabel = self.MakeLabel('Комментарий')
        # для введения комментария
        self.CommField = self.MakeLineEdit('Введи комментарий (опционально)')

        # Кнопка для подтверждения
        self.ExpenseAccept = self.MakeButton('Добавить расход')

        # Соберём в кучку раскладки
        # Разложим сюда строчку ввода данных о покупке
        horiz1 = QtWidgets.QHBoxLayout()
        # Подпись к полю
        horiz1.addWidget(self.ExpenseLabel)
        # Поле ввода
        horiz1.addWidget(self.ExpenseField)

        # Создадим общую вертикальную раскладку
        vert1 = QtWidgets.QVBoxLayout()
        # Добавим в эту вертикальную раскладку первой строкой горизонтальную
        vert1.addLayout(horiz1)

        # Разложим сюда строчку с выбором категории товара
        horiz2 = QtWidgets.QHBoxLayout()
        # Подпись к полю
        horiz2.addWidget(self.CategoryLabel)
        # Выпадающее меню категорий
        horiz2.addWidget(self.CategoryBox)
        # Кнопка изменения списка категорий
        horiz2.addWidget(self.CategoryEditButton)

        # Добавим эту горизонтальную раскладку следующей строкой в вертикальную
        vert1.addLayout(horiz2)

        # Разложим сюда строчку ввода комментария  о покупке
        horiz3 = QtWidgets.QHBoxLayout()
        # Подпись к полю
        horiz3.addWidget(self.CommLabel)
        # Поле ввода
        horiz3.addWidget(self.CommField)

        # Добавим комментарий в раскладку
        vert1.addLayout(horiz3)

        # Добавим в вертикальную раскладку кнопку подтверждения данных
        vert1.addWidget(self.ExpenseAccept)

        # Установим эту раскладку
        self.setLayout(vert1)

        # Займёмся привязкой кнопок
        # Подвяжем кнопку подтверждения добавления расхода к вызову этого добавления
        self.ExpenseAccept.clicked.connect(self.add_expense)
        # Подвяжем кнопку изменения категорий к вызову окна с измененеим этих категорий
        self.CategoryEditButton.clicked.connect(self.ctg_edit_show_window)

        # Добавим категории в общую доступность и в выпадающее окно
        self.set_categories(ctg)

    # Установка категорий: их добавление в выпадающее меню
    def set_categories(self, ctg: list[Category] | None) -> None:
        """Function text is set categories"""
        # Запишем их к себе в класс
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
        # Полагем, что заполняют поле ввода, выбирают категорию,
        # потом подтверждают
        amount = self.ExpenseField.text()
        print('Считано число')
        category = self.CategoryBox.currentText()
        print('Считана категория')
        comm = self.CommField.text()
        print('Считан комментарий')
        # Передаём в создатель
        print('Передаём данные в создатель')
        self.expense_adder(amount, category, comm)
        # Чистим поля
        self.ExpenseField.clear()
        self.CategoryBox.clear()
        self.CommField.clear()

    def ctg_edit_show_window(self):
        """Function text is ctg edit show window"""
        # Запускаем окошко, делая его объектом класса, что создан выше
        self.window2 = CategoryAUDWindow(self.ctg_adder,
                                         self.ctg_updater, self.ctg_deleter)
        # При этом важно его приписать именно в self.windows2, так как при записи
        # в обычную переменную он исчезнет, когда исчезнет и сама переменная.
        self.window2.setWindowTitle('Изменение категорий')
        # Устанавливаем размер
        self.window2.resize(300, 600)
        # Показываем окошко. Без этого оно не отображается
        self.window2.show()

    # Функция создания подписи у чего-либо
    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """Function text is Make Label"""
        # Создаём подпись
        label_obj = QtWidgets.QLabel()
        # Присваиваем ей имя
        label_obj.setText(text)
        return label_obj

    # Функция создания поля с возможностью ввода
    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """Function text is Make Line Edit"""
        # Создаём строку объект строки ввода
        LineEdit_obj = QtWidgets.QLineEdit()
        # Делаем фоновую подпись
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    # Функция создания кнопки
    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """Function text is Make Button"""
        # Создали объект кнопки
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
