import os
import sys
import json
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "db_config.json")

def load_config():
    """Loads database connection config from db_config.json or environment variables."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Failed to read db_config.json: {e}")

    return {
        "db_type": os.getenv("DB_TYPE", "postgresql"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "postgres"),
        "sqlite_path": os.getenv("SQLITE_PATH", "database.db")
    }

def save_config(config_dict):
    """Saves new database connection configuration to db_config.json."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_dict, f, indent=2)
    print(json.dumps({"status": "success", "message": f"Saved config to {CONFIG_FILE}"}))

def get_connection(config=None):
    """Returns database connection based on loaded configuration."""
    if not config:
        config = load_config()
    
    db_type = config.get("db_type", "postgresql").lower()
    
    if db_type == "postgresql":
        return psycopg2.connect(
            dbname=config.get("dbname", "postgres"),
            user=config.get("user", "postgres"),
            password=config.get("password", ""),
            host=config.get("host", "localhost"),
            port=config.get("port", 5432)
        )
    elif db_type == "sqlite":
        sqlite_path = config.get("sqlite_path", "database.db")
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        raise ValueError(f"Unsupported db_type: '{db_type}'. Supported: postgresql, sqlite")

def test_connection():
    """Tests if the database connection can be established."""
    config = load_config()
    try:
        conn = get_connection(config)
        conn.close()
        print(json.dumps({
            "status": "success",
            "message": f"Successfully connected to {config.get('db_type')} database '{config.get('dbname') or config.get('sqlite_path')}'"
        }, indent=2))
        return True
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }, indent=2))
        return False

def get_full_schema():
    """
    Scans the database and returns a complete schema map including:
    - Table names
    - Column names, data types, and nullable flags
    - Sample rows (up to 3) for each table
    """
    config = load_config()
    db_type = config.get("db_type", "postgresql").lower()
    
    schema_info = {
        "db_type": db_type,
        "database": config.get("dbname") or config.get("sqlite_path"),
        "tables": {}
    }
    
    try:
        conn = get_connection(config)
        
        if db_type == "postgresql":
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Fetch all public tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """)
            tables = [row['table_name'] for row in cursor.fetchall()]
            
            for table in tables:
                # Fetch columns
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position;
                """, (table,))
                columns = [dict(col) for col in cursor.fetchall()]
                
                # Fetch sample rows
                cursor.execute(f'SELECT * FROM "{table}" LIMIT 3;')
                sample_rows = [dict(r) for r in cursor.fetchall()]
                
                schema_info["tables"][table] = {
                    "columns": columns,
                    "sample_rows": sample_rows
                }
                
        elif db_type == "sqlite":
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                col_info = cursor.fetchall()
                columns = [
                    {"column_name": col[1], "data_type": col[2], "is_nullable": "YES" if col[3] == 0 else "NO"}
                    for col in col_info
                ]
                
                cursor.execute(f"SELECT * FROM {table} LIMIT 3;")
                sample_rows = [dict(r) for r in cursor.fetchall()]
                
                schema_info["tables"][table] = {
                    "columns": columns,
                    "sample_rows": sample_rows
                }
                
        conn.close()
        print(json.dumps(schema_info, indent=2, default=str))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Failed to get schema: {str(e)}"}, indent=2))

def execute_query(sql_query):
    """Executes any SQL query and prints formatted JSON output."""
    config = load_config()
    db_type = config.get("db_type", "postgresql").lower()
    
    try:
        conn = get_connection(config)
        
        if db_type == "postgresql":
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = conn.cursor()
            
        cursor.execute(sql_query)
        
        if cursor.description:
            rows = cursor.fetchall()
            results = [dict(r) for r in rows]
            conn.close()
            print(json.dumps(results, indent=2, default=str))
        else:
            conn.commit()
            conn.close()
            print(json.dumps({"status": "success", "message": "Query executed successfully."}))
            
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
