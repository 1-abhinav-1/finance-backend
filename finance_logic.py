from collections import defaultdict
from database import insert_expense, get_all_expenses


def analyze_expenses(csv_file):
    import csv

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_expense(
                row["date"],
                row["description"],
                row["category"],
                float(row["amount"]),
            )

    return {"message": "CSV analyzed and stored"}


def analyze_from_db():
    rows = get_all_expenses()

    total = 0
    category_wise = defaultdict(float)

    for _, _, category, amount in rows:
        total += amount
        category_wise[category] += amount

    return {
        "total_expense": round(total, 2),
        "category_wise": dict(category_wise),
    }


def analyze_monthly(year, month):
    rows = get_all_expenses()
    total = 0
    category_wise = defaultdict(float)

    prefix = f"{year}-{str(month).zfill(2)}"

    for date, _, category, amount in rows:
        if date.startswith(prefix):
            total += amount
            category_wise[category] += amount

    return {
        "total_expense": round(total, 2),
        "category_wise": dict(category_wise),
    }


def analyze_category(category_name):
    rows = get_all_expenses()

    transactions = []
    total = 0

    for date, desc, category, amount in rows:
        if category == category_name:
            total += amount
            transactions.append({
                "date": date,
                "description": desc,
                "amount": amount,
            })

    return {
        "total_expense": round(total, 2),
        "transactions": transactions,
    }
