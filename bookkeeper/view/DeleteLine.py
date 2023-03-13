"""
delete line
"""
from PyQt6 import QtWidgets

# Класс, описывающий строку, что удаляет записи расходов из таблицы


class DeleteLine(QtWidgets.QLineEdit):
    """Class representing a DeleteLine"""
    def __init__(self, expense_deleter=None, *args, **kwargs):
        # Всё лишнее на откуп родителю
        super().__init__(*args, **kwargs)
        # Сохраним здесь функцию удаления
        self.expense_deleter = expense_deleter

        # Вводим фоновый текст
        self.setPlaceholderText('Введи ключик расхода на удаление')
        # говорим, что если на клетку нажали дважды,
        # то переходим в функцию, которая будет отслеживать, когда закончим редактирование
        self.textChanged.connect(self.text_is_changing)

    # Обработка события начала изменения текста - ожидаем обработки окончания ввода
    def text_is_changing(self):
        """Function text is changing"""
        self.textChanged.disconnect(self.text_is_changing)
        print('Готовы к удалению. Ожидаем завершения ввода')
        # подключаем после окончания обработки редактирования - обработку результата
        self.editingFinished.connect(self.delete_expense)

    # Обрабатывается окончание редактирования - удаляем расход из таблицы расходов
    def delete_expense(self):
        """Function delete expense"""
        print('Ввод завершён. Начинаем удалять')
        # Отключили отслеживание редактирования
        self.editingFinished.disconnect(self.delete_expense)
        print('Отключили соединение с предыдущей командой')
        # Получили введённый текст
        pk = self.displayText()
        print(f'Получили текст. pk = {pk}')
        # Проверили, что он итоговый
        print('Ключ переведён из текста в int')
        # Заранее чистим ввод
        self.clear()
        self.textChanged.connect(self.text_is_changing)
        self.expense_deleter(pk)
        print('Расход удалён')
