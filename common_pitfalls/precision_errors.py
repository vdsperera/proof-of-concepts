"""_summary_
"""
from decimal import Decimal, getcontext

# initial balance
# Initial balance
balance = Decimal("1000.00")
monthly_interest_rate = Decimal("1.5") / Decimal("100")  # 1.5%

# calculate interest for 12 months
for month in range(1, 13):
    balance += balance * monthly_interest_rate
    print(f"Month {month}: Balance: {balance}")
