"""_summary_
"""

from fastapi_demo.app.models.item_model import Item
from fastapi_demo.app.repositories import item_repository


def create_item(item: Item):
    """_summary_
    """
    if item.price < 0:
        raise ValueError("Item price must be positive.")
    saved_item = item_repository.save_item(item)
    return saved_item


def get_item(item_id: int):
    """_summary_
    """
    item = item_repository.get_item_by_id(item_id)
    if not item:
        raise ValueError(f"Item with ID {item_id} not found.")
    return item
