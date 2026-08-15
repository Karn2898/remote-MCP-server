from fastmcp import FastMCP
import os
import sqlite3
import json

DB_PATH=os.path.join(os.path.dirname(__file__), "expense.db")
CATEGORIES_PATH=os.path.join(os.path.dirname(__file__), "categories.json")
mcp=FastMCP("ExpenseTracker")

with open(CATEGORIES_PATH, "r") as f:
    CATEGORIES = json.load(f)

def init_db():
    with sqlite3.connect(DB_PATH) as c :
        c.execute(""" 
                   CREATE TABLE IF NOT EXISTS expenses (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT NOT NULL,
                       description TEXT NOT NULL,
                       amount REAL NOT NULL,
                       category TEXT NOT NULL,
                       subcategory TEXT DEFAULT '',
                       note TEXT DEFAULT ''
                   )
                   """)

def main():
    init_db()
  



@mcp.tool()
def list_expenses():
    '''List all expenses in the database'''
    with sqlite3.connect(DB_PATH) as c:
        cur=c.execute("SELECT id, date, description, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
        cols=[d[0] for d in cur.description]
        return [dict(zip (cols,r )) for r in cur.fetchall()]
@mcp.tool()
def add_expense(date, description, amount, category, subcategory="", note=""):
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}")
    if subcategory and subcategory not in CATEGORIES[category]:
        raise ValueError(f"Invalid subcategory: {subcategory} for category {category}")
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses (date, description, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?, ?)",
            (date, description, amount, category, subcategory, note)
        )
        c.commit()
    return {"status":"ok","id":cur.lastrowid}
    

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    