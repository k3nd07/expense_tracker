 Personal Expense Tracker (CLI)

A simple, lightweight, and dependency-free command-line interface (CLI) application written in Python to track your personal finances. It allows you to log daily expenses, view visual category breakdowns, and export data for further analysis.

✨ Features

Easy Expense Logging: Quickly record expenses with categories, notes, and dates.

Filtering & Viewing: View all transactions or filter specifically by month.

Visual Statistics:

Visual ASCII bar charts breaking down expenses by category and percentages.

Monthly summaries to track spending trends over time.

Data Persistence: Automatically saves all records to a local expenses.json file.

CSV Export: Export records into a UTF-8 encoded CSV file compatible with Microsoft Excel and Google Sheets.

Zero External Dependencies: Built entirely using standard Python libraries.

🛠️ Requirements

Python 3.7+ (No external packages required)

🚀 Quick Start

Clone the repository:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


Run the application:

python expense_tracker.py


📖 How to Use

When you run the application, you will be presented with a main menu:

=== Трекер расходов ===

1. Добавить расход
2. Показать расходы
3. Удалить расход
4. Статистика по категориям
5. Итоги по месяцам
6. Экспорт в CSV
0. Выход


Options Breakdown

Add Expense: Input amount, select category (Food, Transport, Housing, Entertainment, Health, Clothing, Other), add an optional note, and choose a date (defaults to today).

Show Expenses: View items formatted neatly in a table. Filter by a specific month (MM.YYYY) or view all.

Delete Expense: Remove an entry using its unique ID.

Category Statistics: See total spending by category alongside percentage shares and ASCII progress bars.

Monthly Summaries: View total spending for each month with relative bar charts.

Export to CSV: Generates an expenses_export.csv file inside the program directory.

📁 File Structure

expense_tracker.py — Main application logic and interactive terminal UI.

expenses.json — Auto-generated file storing all transaction records.

expenses_export.csv — Auto-generated CSV output when using the export feature.
