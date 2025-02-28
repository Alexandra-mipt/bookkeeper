"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float = 0
    category: int | None = None
    expense_date: str = datetime.now().isoformat()[:19]
    added_date: str = datetime.now().isoformat()[:19]
    comment: str = ''
    pk: int = 0

    # Оформим красивый вывод для отладки
    def __str__(self) -> str:
        return f'pk = {self.pk}; amount = {self.amount}; category = {self.category};\n' \
               f' exp_date = {self.expense_date}; ' \
               f'add_date = {self.added_date}; comm = {self.comment};'

    def __eq__(self, check: Any) -> bool:
        # Проверим, что совпадают типы
        if not isinstance(check, Expense):
            return NotImplemented
        FTans = ((self.pk == check.pk) & (self.amount == check.amount)
                 and (self.category == check.category)
                 and (self.expense_date == check.expense_date)
                 and (self.added_date == check.added_date)
                 and (self.comment == check.comment))
        return FTans
