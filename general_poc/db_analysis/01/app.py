import asyncio
import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from google.antigravity import Agent, LocalAgentConfig

# =====================================================================
# 1. DATABASE CONFIGURATION & MOCK DATA SETUP
# =====================================================================
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password_here",
    "host": "localhost",
    "port": "5432"
}

def setup_demo_database():
    """Seeds the database with mock tables and data for the demonstration."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create a sample sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_sales (
                id SERIAL PRIMARY KEY,
                region VARCHAR(50),
                category VARCHAR(50),
                revenue NUMERIC(10, 2),
                sale_date DATE
            );
        """)
        
        # Insert sample rows if table is empty
        cursor.execute("SELECT COUNT(*) FROM monthly_sales;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO monthly_sales (region, category, revenue, sale_date) VALUES
                ('North', 'Electronics', 15000.50, '2026-01-15'),
                ('North', 'Furniture', 4200.00, '2026-01-20'),
                ('South', 'Electronics', 22000.00, '2026-02-10'),
                ('South', 'Furniture', 8900.75, '2026-02-14'),
                ('East', 'Electronics', 18500.25, '2026-03-01'),
                ('West', 'Electronics', 31000.00, '2026-03-12');
            """)
            conn.commit()
            print("[Setup] Mock database tables and records initialized.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Setup Error] Make sure PostgreSQL is running: {e}")

# =====================================================================
# 2. AGENT DATABASE TOOL DEFINITION
# =====================================================================
def execute_sql_query(query: str) -> str:
    """
    Executes a SQL query against the PostgreSQL database and returns results as a dictionary list string.
    Use this tool to inspect schema (e.g., SELECT column_name FROM information_schema.columns) or query data.
    """
    print(f"\n[Tool Action] Executing Generated SQL:\n  --> {query}\n")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        
        if cursor.description:
            results = cursor.fetchall()
            conn.close()
            return str([dict(row) for row in results])
        else:
            conn.commit()
            conn.close()
            return "Query executed successfully with no returned rows."
    except Exception as err:
        return f"Database Query Error: {str(err)}"

# =====================================================================
# 3. MAIN AGENT EXECUTION LOOP
# =====================================================================
async def main():
    # 1. Prepare demo database
    setup_demo_database()
    
    # 2. Configure Antigravity Local Agent with Database Tool
    config = LocalAgentConfig(
        system_instructions=(
            "You are an expert Data Analyst AI agent. You have access to a PostgreSQL database "
            "via the `execute_sql_query` tool. First, discover the database schema if needed, "
            "then construct valid SQL queries to answer user data analysis requests."
        ),
        tools=[execute_sql_query]
    )
    
    print("\n--- Starting Antigravity AI Data Analysis Agent ---")
    
    # 3. Determine question from CLI argument or interactive user input
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        print("Enter your question (or press Enter for default question):")
        default_prompt = "What is the total revenue grouped by region for Electronics? Which region performed best?"
        user_input = input("\nQuestion: ").strip()
        user_prompt = user_input if user_input else default_prompt

    # 4. Instantiate Agent Session & Run Analysis
    async with Agent(config) as agent:
        print(f"\nUser Request: '{user_prompt}'\n")
        
        response = await agent.chat(user_prompt)
        
        print("\n--- Final AI Analysis Report ---")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())