"""_summary_
"""

from fastapi_demo.app.models import Item

item_db = {
    1: Item(id=1, name="Laptop", description="A powerful laptop", price=1000.0),
    2: Item(id=2, name="Smartphone", description="A smartphone with a great camera", price=500.0),
    3: Item(id=3, name="Headphones", description="Noise-cancelling headphones", price=200.0),
}

def save_item(item: Item) -> Item:
    """_summary_

    Args:
        item (Item): _description_
    """
    item_db[item.id] = item
    return item

def get_item_by_id(item_id: int) -> Item:
    """_summary_
    """
    print(f"item_repository->get_item_by_id: {item_db.get(item_id)}")
    return item_db.get(item_id)
