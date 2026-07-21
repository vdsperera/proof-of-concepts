"""
Direct Database Query Runner (No External API Key Required)
===========================================================
This runner interacts directly with PostgreSQL using db_tool.
You can run SQL queries directly or ask questions in this chat window.
The Antigravity AI Assistant in this chat session will execute SQL queries,
analyze schema, and generate reports for you directly without any Gemini API key!
"""

import sys
from db_tool import execute_query, get_schema, setup_demo_database

def main():
    setup_demo_database()
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\n[Executing Query]: {query}\n")
        execute_query(query)
    else:
        print("\n--- Direct Database Query Tool ---")
        print("Schema inspect: run 'python app.py schema'")
        print("Run SQL query:  run 'python app.py \"SELECT * FROM monthly_sales;\"'\n")

if __name__ == "__main__":
    main()
