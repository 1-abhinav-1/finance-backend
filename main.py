from fastapi import FastAPI, UploadFile, File
from finance_logic import (
    analyze_expenses,
    analyze_from_db,
    analyze_monthly,
    analyze_category,
)
from database import delete_all_expenses
from database import create_table
from pydantic import BaseModel
from database import insert_expense, delete_all_expenses
from fastapi.middleware.cors import CORSMiddleware
import shutil
import csv
import io

app = FastAPI()

# Create DB table at startup
create_table()

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str
    date: str


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/analyze")
def analyze(file: UploadFile = File(...)):
    with open("uploaded.csv", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return analyze_expenses("uploaded.csv")


@app.get("/summary")
def summary():
    return analyze_from_db()


@app.get("/summary/monthly")
def monthly_summary(year: int, month: int):
    return analyze_monthly(year, month)


@app.get("/summary/category/{category}")
def category_summary(category: str):
    return analyze_category(category)


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    for row in reader:
        analyze_expenses_from_row(row)

    return {"message": "CSV uploaded successfully"}


def analyze_expenses_from_row(row):
    from database import insert_expense

    insert_expense(
        row["date"],
        row["description"],
        row["category"],
        float(row["amount"]),
    )

@app.delete("/expenses")
def clear_expenses():
    delete_all_expenses()
    return {"message": "All expenses cleared"}

@app.post("/expenses")
def add_expense(expense: ExpenseCreate):
    insert_expense(
        expense.date,
        expense.description,
        expense.category,
        expense.amount,
    )
    return {"message": "Expense added successfully"}

@app.delete("/expenses")
def clear_expenses():
    delete_all_expenses()
    return {"message": "All expenses deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
