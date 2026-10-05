"""Трекер расходов.

Возможности:
  - добавление и удаление расходов
  - просмотр списка (все или за выбранный месяц)
  - статистика по категориям с наглядными полосками
  - итоги по месяцам
  - экспорт в CSV (открывается в Excel)
Данные хранятся в файле expenses.json рядом с программой.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")
CSV_FILE = Path(__file__).with_name("expenses_export.csv")

CATEGORIES = ["Еда", "Транспорт", "Жильё", "Развлечения",
              "Здоровье", "Одежда", "Другое"]


@dataclass
class Expense:
    id: int
    date: str        # храним в формате ГГГГ-ММ-ДД, чтобы удобно сортировать
    amount: float
    category: str
    note: str


class ExpenseTracker:
    """Вся логика работы с данными (без ввода/вывода)."""

    def __init__(self, path: Path = DATA_FILE):
        self.path = path
        self.expenses = self._load()

    # ---------- работа с файлом ----------
    def _load(self) -> list:
        if not self.path.exists():
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return [Expense(**item) for item in json.load(f)]
        except (json.JSONDecodeError, TypeError, KeyError):
            print("Файл данных повреждён, начинаем с чистого листа.")
            return []

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in self.expenses], f,
                      ensure_ascii=False, indent=2)

    # ---------- операции ----------
    def add(self, amount: float, category: str, note: str, date: str) -> Expense:
        new_id = max((e.id for e in self.expenses), default=0) + 1
        expense = Expense(new_id, date, amount, category, note)
        self.expenses.append(expense)
        self._save()
        return expense

    def delete(self, expense_id: int) -> bool:
        for e in self.expenses:
            if e.id == expense_id:
                self.expenses.remove(e)
                self._save()
                return True
        return False

    def filter_by_month(self, month: str | None) -> list:
        """month в формате ГГГГ-ММ; None означает «все»."""
        items = self.expenses
        if month:
            items = [e for e in items if e.date.startswith(month)]
        return sorted(items, key=lambda e: (e.date, e.id))

    @staticmethod
    def totals_by_category(items: list) -> dict:
        totals = defaultdict(float)
        for e in items:
            totals[e.category] += e.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def totals_by_month(self) -> dict:
        totals = defaultdict(float)
        for e in self.expenses:
            totals[e.date[:7]] += e.amount
        return dict(sorted(totals.items()))

    def export_csv(self, path: Path = CSV_FILE) -> Path:
        # utf-8-sig и «;» нужны, чтобы Excel правильно открыл русский текст
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID", "Дата", "Сумма", "Категория", "Заметка"])
            for e in self.filter_by_month(None):
                writer.writerow([e.id, fmt_date(e.date), e.amount,
                                 e.category, e.note])
        return path


# ---------- форматирование ----------
def fmt_money(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def fmt_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d.%m.%Y")


def fmt_month(ym: str) -> str:
    return datetime.strptime(ym, "%Y-%m").strftime("%m.%Y")


# ---------- ввод данных с проверкой ----------
def ask_amount() -> float:
    while True:
        raw = input("Сумма: ").replace(",", ".").replace(" ", "")
        try:
            value = float(raw)
            if value <= 0:
                raise ValueError
            return round(value, 2)
        except ValueError:
            print("Введите положительное число, например 450 или 99.90")


def ask_date() -> str:
    while True:
        raw = input("Дата (ДД.ММ.ГГГГ, Enter = сегодня): ").strip()
        if not raw:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(raw, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Неверный формат. Пример: 25.12.2025")


def ask_category() -> str:
    print("Категории:")
    for i, name in enumerate(CATEGORIES, 1):
        print(f"  {i}. {name}")
    while True:
        raw = input("Номер категории: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(CATEGORIES):
            return CATEGORIES[int(raw) - 1]
        print(f"Введите число от 1 до {len(CATEGORIES)}")


def ask_month():
    """Возвращает месяц в формате ГГГГ-ММ или None (все время)."""
    while True:
        raw = input("Месяц (ММ.ГГГГ, Enter = за всё время): ").strip()
        if not raw:
            return None
        try:
            return datetime.strptime(raw, "%m.%Y").strftime("%Y-%m")
        except ValueError:
            print("Неверный формат. Пример: 03.2025")


# ---------- пункты меню ----------
def add_expense(tracker: ExpenseTracker) -> None:
    amount = ask_amount()
    category = ask_category()
    note = input("Заметка (можно пропустить): ").strip()
    date = ask_date()
    e = tracker.add(amount, category, note, date)
    print(f"Добавлено: #{e.id} {fmt_money(e.amount)} ({e.category})")


def show_expenses(tracker: ExpenseTracker) -> None:
    items = tracker.filter_by_month(ask_month())
    if not items:
        print("Расходов не найдено.")
        return
    print(f"\n{'ID':<4} {'Дата':<11} {'Сумма':>12}  {'Категория':<12} Заметка")
    print("-" * 60)
    for e in items:
        print(f"{e.id:<4} {fmt_date(e.date):<11} {fmt_money(e.amount):>12}  "
              f"{e.category:<12} {e.note}")
    print("-" * 60)
    print(f"Итого: {fmt_money(sum(e.amount for e in items))}")


def delete_expense(tracker: ExpenseTracker) -> None:
    raw = input("ID расхода для удаления: ").strip()
    if raw.isdigit() and tracker.delete(int(raw)):
        print("Удалено.")
    else:
        print("Расход с таким ID не найден.")


def show_category_stats(tracker: ExpenseTracker) -> None:
    items = tracker.filter_by_month(ask_month())
    totals = tracker.totals_by_category(items)
    if not totals:
        print("Нет данных для статистики.")
        return
    grand_total = sum(totals.values())
    print()
    for category, value in totals.items():
        share = value / grand_total
        bar = "█" * max(1, round(share * 30))
        print(f"{category:<12} {fmt_money(value):>12}  {share:>5.0%}  {bar}")
    print(f"\nВсего: {fmt_money(grand_total)}")


def show_month_stats(tracker: ExpenseTracker) -> None:
    totals = tracker.totals_by_month()
    if not totals:
        print("Нет данных для статистики.")
        return
    biggest = max(totals.values())
    print()
    for month, value in totals.items():
        bar = "█" * max(1, round(value / biggest * 30))
        print(f"{fmt_month(month)}  {fmt_money(value):>12}  {bar}")


def export_to_csv(tracker: ExpenseTracker) -> None:
    path = tracker.export_csv()
    print(f"Экспортировано в файл: {path}")


MENU = [
    ("Добавить расход", add_expense),
    ("Показать расходы", show_expenses),
    ("Удалить расход", delete_expense),
    ("Статистика по категориям", show_category_stats),
    ("Итоги по месяцам", show_month_stats),
    ("Экспорт в CSV", export_to_csv),
]


def main() -> None:
    tracker = ExpenseTracker()
    print("=== Трекер расходов ===")
    while True:
        print()
        for i, (title, _) in enumerate(MENU, 1):
            print(f"{i}. {title}")
        print("0. Выход")
        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            print("До встречи!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            print()
            MENU[int(choice) - 1][1](tracker)
        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
