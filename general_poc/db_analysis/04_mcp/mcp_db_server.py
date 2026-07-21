"""
PostgreSQL Model Context Protocol (MCP) Server
===============================================
Exposes standardized MCP tools over stdio for database inspection & query execution.
"""

import os
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Postgres-DB-Analyzer")

def get_db_config():
    return {
        "dbname": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "your_password_here"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432")
    }

def get_connection():
    return psycopg2.connect(**get_db_config())

@mcp.tool()
def list_tables() -> str:
    """Lists all available tables in the PostgreSQL database public schema."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return json.dumps({"status": "success", "tables": tables}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Describes columns, data types, and nullability for a given table."""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return json.dumps({"status": "success", "table": table_name, "columns": columns}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
def execute_sql(sql_query: str) -> str:
    """Executes a SQL SELECT query against PostgreSQL and returns results as JSON."""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql_query)
        
        if cursor.description:
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            conn.close()
            return json.dumps(results, indent=2, default=str)
        else:
            conn.commit()
            conn.close()
            return json.dumps({"status": "success", "message": "Query executed successfully."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # Runs the MCP server listening on stdio
    mcp.run()
