import pandas as pd
from langchain.tools import tool
from typing import Optional
import os


@tool
def summarise_expenses(filepath: str, month: Optional[str] = None) -> str:
    """
    Summarise expenses from a CSV file.
    The CSV must have columns: date, category, amount, description.
    Optionally filter by month (e.g. '2025-03').
    """
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    try:
        df = pd.read_csv(filepath, parse_dates=["date"])
    except Exception as e:
        return f"Error reading CSV: {e}"

    if month:
        df = df[df["date"].dt.to_period("M").astype(str) == month]
        if df.empty:
            return f"No data found for month: {month}"

    total = df["amount"].sum()
    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    lines = [f"Total expenses: £{total:,.2f}", ""]
    lines.append("Breakdown by category:")
    for cat, amt in by_category.items():
        lines.append(f"  {cat}: £{amt:,.2f}")

    return "\n".join(lines)


@tool
def list_outstanding_invoices(filepath: str) -> str:
    """
    List all unpaid invoices from a CSV file.
    The CSV must have columns: invoice_id, client, amount, due_date, status.
    """
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    try:
        df = pd.read_csv(filepath, parse_dates=["due_date"])
    except Exception as e:
        return f"Error reading CSV: {e}"

    unpaid = df[df["status"].str.lower() != "paid"]
    if unpaid.empty:
        return "No outstanding invoices found."

    total_owed = unpaid["amount"].sum()
    lines = [f"Outstanding invoices: {len(unpaid)} | Total owed: £{total_owed:,.2f}", ""]
    for _, row in unpaid.iterrows():
        lines.append(
            f"• {row['invoice_id']} — {row['client']} — £{row['amount']:,.2f} — Due: {row['due_date'].date()}"
        )
    return "\n".join(lines)


def get_finance_tools():
    return [summarise_expenses, list_outstanding_invoices]
