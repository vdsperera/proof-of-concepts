"""_summary_
"""

from pydantic import BaseModel

class Item(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: int
    name: str
    description: str
    price: float
