"""
MCP Client & Agent Integration Demo
====================================
Demonstrates how an AI Agent:
 1. Reads Codebase Domain Rules (from models.py)
 2. Connects to the Postgres MCP Server via Stdio
 3. Discovers MCP Tools & Executes SQL Queries
 4. Combines Codebase Rules + MCP Data for accurate business reporting
"""

import os
import sys
import json
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Import local codebase models to demonstrate code-aware analysis
from models import OrderStatus, get_net_revenue

async def run_mcp_agent():
    # Define server launch configuration
    server_script = os.path.join(os.path.dirname(__file__), "mcp_db_server.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy()
    )

    print("\n--- Connecting to Postgres MCP Server over Stdio ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize MCP Protocol
            await session.initialize()
            print("[MCP] Protocol session initialized successfully.")
            
            # 2. Discover Available MCP Tools
            tools_response = await session.list_tools()
            available_tools = [tool.name for tool in tools_response.tools]
            print(f"[MCP] Discovered Tools: {available_tools}\n")
            
            # 3. Agent inspects codebase context from models.py:
            #    - OrderStatus.COMPLETED = 2
            #    - is_test_order MUST be false
            print("[Codebase Context] Inspected 'models.py':")
            print(f"  • COMPLETED Order Status Code = {int(OrderStatus.COMPLETED)} ({OrderStatus.COMPLETED.name})")
            print("  • Rule: Exclude test orders (is_test_order = false)\n")

            # 4. Agent calls MCP 'execute_sql' Tool using codebase-aware SQL:
            sql_query = f"""
                SELECT 
                    id, 
                    customer_id, 
                    gross_amount, 
                    discount_rate 
                FROM orders 
                WHERE status = {int(OrderStatus.COMPLETED)} 
                  AND is_test_order = false;
            """
            
            print(f"[Agent -> MCP Server] Executing SQL Tool:\n{sql_query.strip()}\n")
            
            tool_result = await session.call_tool("execute_sql", arguments={"sql_query": sql_query})
            raw_data = json.loads(tool_result.content[0].text)
            
            print(f"[MCP Server Response]: Returned {len(raw_data)} completed non-test orders.\n")
            
            # 5. Agent applies domain logic (get_net_revenue) from codebase to calculating final metrics:
            total_gross = 0.0
            total_net = 0.0
            
            print("--- Analysis Report (Code + DB Unified) ---")
            for row in raw_data:
                gross = float(row["gross_amount"])
                rate = float(row["discount_rate"])
                net = get_net_revenue(gross, rate)
                total_gross += gross
                total_net += net
                print(f"  • Order #{row['id']}: Gross ${gross:.2f} (Discount {rate*100:.0f}%) -> Net ${net:.2f}")
                
            print("-" * 50)
            print(f"Total Gross Revenue : ${total_gross:,.2f}")
            print(f"Total Net Revenue   : ${total_net:,.2f}")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(run_mcp_agent())
