"""
box
"""
from PyQt6 import QtWidgets

# Класс выпадающего списка


class EasyComboBox(QtWidgets.QComboBox):
    """Class representing a EasyComboBox"""
    def __init__(self, *args, **kwargs):
        # Передадим всё лишнее родителю
        super().__init__(*args, **kwargs)
        self.clear()
        self.set_items()

    def clear(self):
        """Function text is clear"""
        self.setCurrentText(self.placeholderText())

    # Составляем начинку выпадающего списка
    def set_items(self, text_for_items: list[str] = ['empty']) -> None:
        """Function text is set items"""
        self.clear()
        print('В теории, список должен был очиститься')
        super(EasyComboBox, self).clear()
        print('Совсем мощно должен был очиститься')
        if (isinstance(text_for_items, str)) | (text_for_items == []):
            raise ValueError('Неверный ввод!')

        # Составим его содержимое
        for name in text_for_items:
            print(f'Добавлено окошко {name}')
            self.addItem(name)
