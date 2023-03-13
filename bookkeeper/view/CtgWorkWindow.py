"""
work window
"""
from PyQt6 import QtWidgets, QtGui

# Создадим окно редактирования категории


class CategoryAUDWindow(QtWidgets.QWidget):
    """Class representing a CategoryAUDWindow"""
    def __init__(self,
                 ctg_adder=None,
                 ctg_updater=None,
                 ctg_deleter=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Выполнен вход в окно редактирования категорий')
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter

        # Создадим подпись
        self.ButtonLabel = self.MakeLabel('Выбери один из вариантов')

        # Создания
        self.CtgAddCheck = self.MakeButton('Создать категорию')
        # Обновления
        self.CtgUpdCheck = self.MakeButton('Обновить категорию')
        # Удаления
        self.CtgDelCheck = self.MakeButton('Удалить категорию')

        # Имя категории
        self.CtgName = self.MakeLineEdit('Введи имя категории БЕЗ ПРОБЕЛОВ. '
                                         'Чувствителен к регистру.')
        # Родитель категории
        self.CtgParent = self.MakeLineEdit('Введи имя родителя БЕЗ ПРОБЕЛОВ. '
                                           'Чувствителен к регистру.')
        # Дети
        self.CtgChildrens = self.MakeLineEdit('Введи имена детей через пробелы.'
                                              ' (На свой страх и риск)')

        # Создадим кнопку подтверждения
        self.AcceptButton = self.MakeButton('Подтвердить')

        # поле для картинки
        self.PicField = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('Python.png')
        print(self.pixmap.isNull())
        self.PicField.setPixmap(self.pixmap)
        self.PicField.setScaledContents(True)
        self.PicField.setMaximumWidth(650)
        self.PicField.setMaximumHeight(600)

        # Вертикальная раскладка
        vert = QtWidgets.QVBoxLayout()
        # Добавим картинку
        vert.addWidget(self.PicField)
        # Добавим подпись
        vert.addWidget(self.ButtonLabel)

        # Ряд кнопок
        horiz = QtWidgets.QHBoxLayout()
        # Кнопки
        horiz.addWidget(self.CtgAddCheck)
        horiz.addWidget(self.CtgUpdCheck)
        horiz.addWidget(self.CtgDelCheck)

        vert.addLayout(horiz)

        # Добавим поля ввода
        vert.addWidget(self.CtgName)
        vert.addWidget(self.CtgParent)
        vert.addWidget(self.CtgChildrens)

        vert.addWidget(self.AcceptButton)

        self.setLayout(vert)

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        # Привяжем верхние кнопки к действиям
        self.CtgAddCheck.clicked.connect(self.ctg_add1)
        self.CtgUpdCheck.clicked.connect(self.ctg_upd1)
        self.CtgDelCheck.clicked.connect(self.ctg_del1)

        print('Окно сформировано')

    # Добавление часть 1
    def ctg_add1(self):
        """Function ctg_add1"""
        print('Вошли в режим добавления')

        # Заблокируем остальные кнопки и разблокируем заблокированные
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_add2)

    # Добавление часть 2
    def ctg_add2(self):
        """Function ctg_add2"""
        self.AcceptButton.clicked.disconnect(self.ctg_add2)
        print('Начат второй этап добавления')
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, {self.CtgChildrens.text()}')
        self.ctg_adder(self.CtgName.text(),
                       self.CtgParent.text(), self.CtgChildrens.text())
        print('Добавление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        # Вернём кнопки в исходное состояние
        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Добавление завершено. Сброс до исходного состояния произведён.')

    # обновление часть 1
    def ctg_upd1(self):
        """Function ctg_upd1"""
        print('Вошли в режим обновления')
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_upd2)

    # обновление часть 2
    def ctg_upd2(self):
        """Function ctg_upd2"""
        self.AcceptButton.clicked.disconnect(self.ctg_upd2)
        print('Начат второй этап обновления')
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, {self.CtgChildrens.text()}')
        self.ctg_updater(self.CtgName.text(),
                         self.CtgParent.text(), self.CtgChildrens.text())
        print('Обновление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Обновление завершено. Сброс до исходного состояния произведён.')

    # Удаление часть 1
    def ctg_del1(self):
        """Function ctg_del1"""
        print('Вошли в режим удаления')
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_del2)

    # Удаление часть 2
    def ctg_del2(self):
        """Function ctg_del2"""
        self.AcceptButton.clicked.disconnect(self.ctg_del2)
        print('Начат второй этап удаления')
        print(f'{self.CtgName.text()}')
        self.ctg_deleter(self.CtgName.text())
        print('Удаление в БД выполнено')
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Удаление завершено. Сброс до исходного состояния произведён.')

    # Функция создания подписи у чего-либо
    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """Function MakeLabel"""
        label_obj = QtWidgets.QLabel()
        label_obj.setText(text)
        return label_obj

    # Функция создания поля с возможностью ввода
    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """Function MakeLineEdit"""
        LineEdit_obj = QtWidgets.QLineEdit()
        LineEdit_obj.setPlaceholderText(text)
        return LineEdit_obj

    # Функция создания кнопки
    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """Function MakeButton"""
        Button_obj = QtWidgets.QPushButton(text)
        return Button_obj
