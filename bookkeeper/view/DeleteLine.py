"""
delete line
"""
from PyQt6 import QtWidgets

# Класс, описывающий строку, что удаляет записи расходов из таблицы


class DeleteLine(QtWidgets.QLineEdit):
    """Class representing a DeleteLine"""
    def __init__(self, expense_deleter=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expense_deleter = expense_deleter

        # Вводим фоновый текст
        self.setPlaceholderText('Введи ключик расхода на удаление')
        self.textChanged.connect(self.text_is_changing)

    # Обработка события начала изменения текста - ожидаем обработки окончания ввода
    def text_is_changing(self):
        """Function text is changing"""
        self.textChanged.disconnect(self.text_is_changing)
        print('Готовы к удалению. Ожидаем завершения ввода')
        self.editingFinished.connect(self.delete_expense)

    # Обрабатывается окончание редактирования - удаляем расход из таблицы расходов
    def delete_expense(self):
        """Function delete expense"""
        print('Ввод завершён. Начинаем удалять')
        self.editingFinished.disconnect(self.delete_expense)
        print('Отключили соединение с предыдущей командой')
        pk = self.displayText()
        print(f'Получили текст. pk = {pk}')
        print('Ключ переведён из текста в int')
        self.clear()
        self.textChanged.connect(self.text_is_changing)
        self.expense_deleter(pk)
        print('Расход удалён')
