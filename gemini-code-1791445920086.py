import pandas as pd

def calculate_budget_summary(df: pd.DataFrame, monthly_income: float) -> dict:
    if df.empty:
        total_expenses = 0.0
        expenses_by_cat = {}
    else:
        expenses_df = df[df["type"] == "expense"]
        total_expenses = float(expenses_df["amount"].sum())
        expenses_by_cat = expenses_df.groupby("category")["amount"].sum().to_dict()

    remaining_budget = monthly_income - total_expenses
    savings_rate = ((monthly_income - total_expenses) / monthly_income * 100) if monthly_income > 0 else 0.0

    return {
        "monthly_income": monthly_income,
        "total_expenses": total_expenses,
        "remaining_budget": remaining_budget,
        "savings_rate": max(0.0, savings_rate),
        "category_breakdown": expenses_by_cat
    }