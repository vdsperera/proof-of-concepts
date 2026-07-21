"""
Application Domain Models & Business Rules
==========================================
This file represents the project's codebase business logic context.
An AI agent inspects this code to understand what table values & statuses mean.
"""

from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime

class OrderStatus(IntEnum):
    PENDING = 1
    COMPLETED = 2
    REFUNDED = 3
    CANCELLED = 4

class CustomerTier(IntEnum):
    STANDARD = 1
    PREMIUM = 2
    VIP = 3

@dataclass
class Order:
    id: int
    customer_id: int
    status: OrderStatus
    gross_amount: float
    discount_rate: float  # e.g. 0.10 for 10%
    is_test_order: bool   # Test orders should be excluded from financial analytics!
    created_at: datetime

def get_net_revenue(gross_amount: float, discount_rate: float) -> float:
    """Calculates actual net revenue after discount."""
    return gross_amount * (1.0 - discount_rate)
