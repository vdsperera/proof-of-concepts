import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# =====================================================================
# DATABASE CONFIGURATION
# =====================================================================
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password_here",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def setup_demo_database():
    """Seeds the database with sample monthly_sales data if not already present."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_sales (
                id SERIAL PRIMARY KEY,
                region VARCHAR(50),
                category VARCHAR(50),
                revenue NUMERIC(10, 2),
                sale_date DATE
            );
        """)
        
        cursor.execute("SELECT COUNT(*) FROM monthly_sales;")
        count = cursor.fetchone()[0]
        if count == 0:
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
            print("[Setup] Mock database tables and records initialized successfully.")
        else:
            print(f"[Setup] Table 'monthly_sales' already exists with {count} records.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Database Error] Failed to connect/setup database: {e}")

def get_schema():
    """Inspects and returns database schema details for public tables."""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable
            FROM information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
            WHERE t.table_schema = 'public'
            ORDER BY t.table_name, c.ordinal_position;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        schema_map = {}
        for row in rows:
            table = row['table_name']
            if table not in schema_map:
                schema_map[table] = []
            schema_map[table].append({
                "column": row['column_name'],
                "type": row['data_type'],
                "nullable": row['is_nullable']
            })
            
        conn.close()
        print(json.dumps(schema_map, indent=2, default=str))
    except Exception as e:
        print(f"[Schema Error] {e}")

def execute_query(sql_query: str):
    """Executes SQL query against PostgreSQL and outputs results as JSON."""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql_query)
        
        if cursor.description:
            results = cursor.fetchall()
            conn.close()
            # Format datetime/decimal to string for clean JSON output
            clean_results = [dict(row) for row in results]
            print(json.dumps(clean_results, indent=2, default=str))
        else:
            conn.commit()
            conn.close()
            print(json.dumps({"status": "success", "message": "Query executed successfully with no returned rows."}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

def print_help():
    print("""
PostgreSQL Database Analysis CLI Tool (02)
------------------------------------------
Usage:
  python db_tool.py setup             - Initializes demo database table & data
  python db_tool.py schema            - Shows public database schema as JSON
  python db_tool.py query "<SQL>"     - Executes a SQL query and returns JSON output
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "setup":
        setup_demo_database()
    elif cmd == "schema":
        get_schema()
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("[Error] Missing SQL query argument. Usage: python db_tool.py query \"SELECT ...\"")
            sys.exit(1)
        sql = " ".join(sys.argv[2:])
        execute_query(sql)
    else:
        print_help()

if __name__ == "__main__":
    main()
