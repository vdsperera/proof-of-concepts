# Approach 1: Model Context Protocol (MCP) Demo (`04_mcp`)

This folder demonstrates **Approach 1 (Model Context Protocol - MCP)**, showing how modern AI coding agents combine **Codebase Context** + **Database Execution Tools** to perform business-aware database analytics.

---

## 🎯 Key Architecture Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                 AI Agent / Assistant Context                │
├──────────────────────────────┬──────────────────────────────┤
│    1. Codebase Knowledge     │     2. MCP Database Tool     │
│   (models.py & enums.py)     │    (mcp_db_server.py)       │
├──────────────────────────────┴──────────────────────────────┤
│  • Knows status code 2 = COMPLETED                          │
│  • Knows to exclude test orders (is_test_order = false)     │
│  • Applies net_revenue = gross * (1 - discount)             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼ Executes over stdio JSON-RPC
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Files in `04_mcp/`

- **[models.py](file:///c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/models.py)**: Codebase domain models (`OrderStatus`, `CustomerTier`, `get_net_revenue()`).
- **[mcp_db_server.py](file:///c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/mcp_db_server.py)**: FastMCP Server exposing `list_tables`, `describe_table`, and `execute_sql` over stdio.
- **[seed_mcp_db.py](file:///c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/seed_mcp_db.py)**: Database seeder script.
- **[mcp_client_agent.py](file:///c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/mcp_client_agent.py)**: MCP client demonstrating tool discovery and unified code-database analysis.
- **[mcp_config.json](file:///c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/mcp_config.json)**: Standard MCP configuration JSON for registering servers in IDEs.

---

## 🚀 How to Run the Included Demo

1. **Seed the database table**:
   ```powershell
   python .\general_poc\db_analysis\04_mcp\seed_mcp_db.py
   ```

2. **Run the MCP Agent Client**:
   ```powershell
   python .\general_poc\db_analysis\04_mcp\mcp_client_agent.py
   ```

---

## 💼 Practical Production Setup (How to Use in Daily Development)

### 1. Registering the Server in Your IDE / AI Tool
In modern AI coding tools (Antigravity, Cursor, Claude Desktop), add the server block to your IDE config or settings JSON:

```json
{
  "mcpServers": {
    "postgres-db": {
      "command": "python",
      "args": [
        "c:/Activities/Projects/proof-of-concepts/general_poc/db_analysis/04_mcp/mcp_db_server.py"
      ],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_NAME": "postgres",
        "DB_PASSWORD": "your_password_here"
      }
    }
  }
}
```

---

### 2. Production Ready Open-Source Servers (Zero Custom Code!)
In real production projects, you can use official community servers without writing custom Python code:

```json
{
  "mcpServers": {
    "postgres-official": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://postgres:your_password@localhost:5432/postgres"
      ]
    },
    "sqlite-official": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./database.db"]
    }
  }
}
```

---

### 3. Real-World Practical Prompts

Once configured, simply chat naturally in your IDE:

- **Business Revenue Analysis**:
  > *"Look at `models.py` to see how `OrderStatus` is defined, then query the database via MCP to calculate net revenue for completed orders."*

- **Customer Issue Debugging**:
  > *"Customer ID 103 reported an issue. Check `models.py` for status enums and query order #103 in the database."*

- **Schema Drift Check**:
  > *"Compare column names in `models.py` against the `orders` table schema via MCP `describe_table` to check if migrations are needed."*
