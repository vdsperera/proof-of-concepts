# Generic Database Analysis Suite (`03`)

A flexible database inspection and analysis tool that can connect to **ANY database** (PostgreSQL, SQLite, etc.) and allows analyzing any database schema & answering natural language questions without external API keys.

---

## 🚀 Features
- **Multi-Database Support**: Connects to PostgreSQL, SQLite, etc.
- **Dynamic Schema Discovery**: Auto-detects all tables, column types, and sample rows.
- **No External API Keys Required**: Integrates directly with the Antigravity chat agent.
- **Configurable Connection**: Save custom host, port, credentials, or SQLite paths via CLI or `db_config.json`.

---

## 🛠️ Commands & Usage

### 1. Set Database Connection Config
```powershell
# PostgreSQL Example
python app.py set-config --type postgresql --host localhost --port 5432 --user postgres --pass your_password --db your_db_name

# SQLite Example
python app.py set-config --type sqlite --sqlite-path "C:\path\to\your_database.db"
```

### 2. Test Database Connection
```powershell
python app.py test
```

### 3. Scan & Discover Full Database Schema
```powershell
python app.py schema
```

### 4. Run Any SQL Query
```powershell
python app.py query "SELECT * FROM your_table_name LIMIT 10;"
```

---

## 💬 How to use via Chat Window
Simply set your connection configuration, then ask any question in this chat window!
- *"What are all tables in my database?"*
- *"Show top 5 customers by order count"*
- *"Compare monthly revenue for 2026"*
