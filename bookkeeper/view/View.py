"""
view of app
"""
import sys
from typing import Protocol
from collections.abc import Callable
from PyQt6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from bookkeeper.view.Window import BookkeeperWindow
from bookkeeper.view.CtgWorkWindow import CategoryAUDWindow


class AbstractView(Protocol):
    """Class representing a Abstract View"""
    def show_main_window(self) -> None:
        """Function shows main window"""

    def set_categories(self, ctg: list[Category]) -> None:
        """Function is set categories"""

    def set_expenses(self, ctg: list[Expense]) -> None:
        """Function is set expenses"""

    def set_budgets(self, ctg: list[Budget]) -> None:
        """Function is set budgets"""

    def set_ctg_adder(self, handler: Callable[[str, str], None]) -> None:
        """Function shows main window"""

    def set_ctg_deleter(self, handler: Callable[[str], None]) -> None:
        """Function is set_ctg_adder"""

    def set_ctg_checker(self, handler: Callable[[str], None]) -> None:
        """Function is set_ctg_checker"""

    def set_ctg_updater(self, handler: Callable[[str, str, str | None], None]) -> None:
        """Function is set_ctg_updater"""

    def set_bdg_modifier(self, handler: Callable[['int | None', str, str], None]) -> None:
        """Function is set_bdg_modifier"""

    def set_exp_adder(self, handler: Callable[[str, str, str], None]) -> None:
        """Function is set_exp_adder"""

    def set_exp_deleter(self, handler: Callable[[str], None]) -> None:
        """Function is set_exp_deleter"""

    def set_exp_updater(self, handler: Callable[[int, list[str],
                                                 list[str]], None]) -> None:
        """Function is set_exp_updater"""


def handle_error(widget, handler):
    """Function handle_error"""
    def inner(*args, **kwargs):
        """Function is inner"""
        try:
            handler(*args, **kwargs)
        except ValueError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner


class View:
    """Class representing a view"""
    categories: list[Category] = [Category(name='Empty_Cat')]

    def __init__(self):
        # Запускаем приложение. Без этого ничего не будет работать
        print('Запуск приложения начат')
        self.app = QtWidgets.QApplication(sys.argv)
        # Заполняем поля категорий
        self.config_ctg_edit()
        # Запускаем окно
        self.main_window = BookkeeperWindow(self.categories,
                                            self.add_expense,
                                            self.update_expense,
                                            self.delete_expenses,
                                            self.ctg_pk_2_name,
                                            self.add_category,
                                            self.update_category,
                                            self.delete_category,
                                            self.modify_budget)
        print('Окно запущено')
        # Отразмериваем
        self.main_window.resize(1200, 700)
        self.main_window.setWindowTitle('Чёрная бухгалтерия')

    # Функция запуска основного окна
    def show_main_window(self):
        """Function shows main window"""
        self.main_window.show()

        # Вступительное оповещение
        dlg = QtWidgets.QMessageBox(self.main_window)
        dlg.setWindowTitle('Пользовательское соглашение')
        dlg.setText('Примите пользовательское соглашение, по которому обязуетесь  \n'
                    'вводить в приложение только правду, иначе до следующего раза!')
        dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes |
                               QtWidgets.QMessageBox.StandardButton.No)
        button = dlg.exec()
        if button == QtWidgets.QMessageBox.StandardButton.No:
            sys.exit()

        print('Приложение запущено')
        print(f'Application ends with exit status {self.app.exec()}')
        sys.exit()

    def config_ctg_edit(self):
        """Function config_ctg_edit"""
        self.ctg_edit_window = CategoryAUDWindow(self.add_category,
                                                 self.update_category,
                                                 self.delete_category)
        self.ctg_edit_window.setWindowTitle("Редактирование категорий")
        self.ctg_edit_window.resize(600, 300)

    # Отдельная функция на запуск окна настроек категорий
    def ctg_edit_show(self):
        """Function ctg_edit_show"""
        self.ctg_edit_window.show()

    def set_categories(self, ctg: list[Category]) -> None:
        """Function set_categories"""
        self.categories = ctg
        self.main_window.ExpenseAndCategoryEdit.set_categories(self.categories)

    def ctg_pk_2_name(self, pk: int | None) -> str:
        """Function ctg_pk_2_name"""
        if pk is None:
            return 'Empty'
        name = [c.name for c in self.categories if int(c.pk) == int(pk)]
        if len(name):
            return str(name[0])

    def set_ctg_updater(self, handler):
        """Function set_ctg_updater"""
        self.ctg_updater = handle_error(self.main_window, handler)

    def set_ctg_adder(self, handler):
        """ устанавливает метод добавления категории (из bookkeeper_app)"""
        self.ctg_adder = handle_error(self.main_window, handler)

    def set_ctg_deleter(self, handler):
        """ устанавливает метод удаления категории (из bookkeeper_app)"""
        self.ctg_deleter = handle_error(self.main_window, handler)

    def set_ctg_checker(self, handler):
        """ устанавливает метод проверки существования категории (из bookkeeper_app)"""
        self.ctg_checker = handle_error(self.main_window, handler)

    def add_category(self, name, parent, children):
        """Function shows main window"""
        self.ctg_adder(name, parent, children)

    def update_category(self, name, parent, children):
        """Function adds category"""
        self.ctg_updater(name, parent, children)

    def delete_category(self, ctg_name: str):
        """Function deletes category"""
        self.ctg_deleter(ctg_name)

    def set_expenses(self, exps: list[Expense]) -> None:
        """Function set_expenses"""
        self.expenses = exps
        self.main_window.ExpensesTable.set_expenses(self.expenses)

    def set_exp_adder(self, handler):
        """ устанавливает метод добавления траты (из bookkeeper_app)"""
        self.exp_adder = handle_error(self.main_window, handler)

    def set_exp_deleter(self, handler):
        """ устанавливает метод удаления трат (из bookkeeper_app)"""
        self.exp_deleter = handle_error(self.main_window, handler)

    def set_exp_updater(self, handler):
        """ устанавливает метод изменения траты (из bookkeeper_app)"""
        self.exp_updater = handle_error(self.main_window, handler)

    def add_expense(self, amount: str, ctg_name: str, comment: str = ""):
        """Function add_expensew"""
        self.exp_adder(amount, ctg_name, comment)

    def delete_expenses(self, pk: str):
        """Function delete_expenses"""
        dlg = QtWidgets.QMessageBox(self.main_window)
        dlg.setWindowTitle('Удаление')
        dlg.setText('Удалить расход?')
        dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes |
                               QtWidgets.QMessageBox.StandardButton.No)
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Question)

        button = dlg.exec()

        if button == QtWidgets.QMessageBox.StandardButton.Yes:
            self.exp_deleter(pk)

    def update_expense(self, pk, attr, new_val):
        """Function update_expense"""
        self.exp_updater(pk, attr, new_val)

    def set_budgets(self, budgets: list[Budget]) -> None:
        """Function shows set_budgets"""
        self.budgets = budgets
        self.main_window.BudgetTable.set_budgets(self.budgets)

    def set_bdg_modifier(self, handler):
        """ устанавливает метод изменения бюджета (из bookkeeper_app)"""
        self.bdg_modifier = handle_error(self.main_window, handler)

    def modify_budget(self, pk: int, new_limit: str, period: str):
        """Function modify_budget"""
        self.bdg_modifier(pk, new_limit, period)
