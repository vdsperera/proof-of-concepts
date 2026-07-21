"""
Seeds the database with orders data reflecting models.py domain logic.
"""

import os
import psycopg2

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def seed():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INT,
                status INT, -- 1=PENDING, 2=COMPLETED, 3=REFUNDED, 4=CANCELLED
                gross_amount NUMERIC(10, 2),
                discount_rate NUMERIC(4, 2),
                is_test_order BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("SELECT COUNT(*) FROM orders;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO orders (customer_id, status, gross_amount, discount_rate, is_test_order, created_at) VALUES
                (101, 2, 1000.00, 0.10, false, '2026-03-01 10:00:00'), -- Net: 900 (COMPLETED)
                (102, 2, 2500.00, 0.20, false, '2026-03-02 11:30:00'), -- Net: 2000 (COMPLETED)
                (103, 3, 1500.00, 0.00, false, '2026-03-03 14:15:00'), -- REFUNDED! Should be excluded from revenue
                (104, 2, 5000.00, 0.00, true,  '2026-03-04 16:00:00'), -- TEST ORDER! Should be excluded from financial metrics
                (105, 2, 3000.00, 0.05, false, '2026-03-05 09:45:00'); -- Net: 2850 (COMPLETED)
            """)
            conn.commit()
            print("[Seed] Successfully created and populated 'orders' table for MCP demo.")
        else:
            print("[Seed] 'orders' table already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Seed Error] {e}")

if __name__ == "__main__":
    seed()
