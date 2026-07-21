"""
Generic Database Analysis Suite (03)
=====================================
Analyzes ANY database (PostgreSQL, SQLite, etc.) dynamically.

Usage:
  1. Configure connection:
     python app.py set-config --type postgresql --host localhost --user postgres --pass your_password --db postgres
     
  2. Test connection:
     python app.py test
     
  3. Scan & print schema of all tables:
     python app.py schema
     
  4. Run any SQL query:
     python app.py query "SELECT * FROM <any_table>;"
"""

import argparse
from db_analyzer import load_config, save_config, test_connection, get_full_schema, execute_query

def main():
    parser = argparse.ArgumentParser(description="Generic Database Analyzer Suite")
    subparsers = parser.add_subparsers(dest="command")
    
    # Subcommand: set-config
    config_parser = subparsers.add_parser("set-config", help="Set database connection parameters")
    config_parser.add_argument("--type", choices=["postgresql", "sqlite"], default="postgresql", help="Database type")
    config_parser.add_argument("--host", default="localhost", help="Database host")
    config_parser.add_argument("--port", type=int, default=5432, help="Database port")
    config_parser.add_argument("--user", default="postgres", help="Database user")
    config_parser.add_argument("--pass", dest="password", default="", help="Database password")
    config_parser.add_argument("--db", dest="dbname", default="postgres", help="Database name")
    config_parser.add_argument("--sqlite-path", default="database.db", help="SQLite file path if type is sqlite")
    
    # Subcommand: test
    subparsers.add_parser("test", help="Test database connection")
    
    # Subcommand: schema
    subparsers.add_parser("schema", help="Get schema & sample rows for all tables")
    
    # Subcommand: query
    query_parser = subparsers.add_parser("query", help="Execute SQL query")
    query_parser.add_argument("sql", nargs="+", help="SQL statement to execute")
    
    args = parser.parse_args()
    
    if args.command == "set-config":
        new_config = {
            "db_type": args.type,
            "host": args.host,
            "port": args.port,
            "user": args.user,
            "password": args.password,
            "dbname": args.dbname,
            "sqlite_path": args.sqlite_path
        }
        save_config(new_config)
    elif args.command == "test":
        test_connection()
    elif args.command == "schema":
        get_full_schema()
    elif args.command == "query":
        sql_str = " ".join(args.sql)
        execute_query(sql_str)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
