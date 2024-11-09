"""
4. Catching at the Top Level (Centralized Handling)

What It Is:
    Catching exceptions at the entry point (e.g., main() function),
    handling errors globally, and ensuring the program doesn’t crash.

How It’s Done:
    Use a try-except block in your main entry point, capturing all
    exceptions to handle them in a centralized way (logging, user
    notification, etc.).

When to Use:
    In applications where you want to ensure graceful error handling
    and logging, or where you want a single place to deal with unexpected
    issues.
"""

import traceback

class DatabaseError(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

class ItemNotFoundError(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

def database_load(item_id):
    """_summary_

    Args:
        item_id (_type_): _description_
    """
    if item_id < 0:
        raise DatabaseError("Database connection failed")
    elif item_id == 0:
        raise ItemNotFoundError("Item not found")
    else:
        return {"id": item_id, "name": "Item name"}


def load_data_centralized(item_id):
    """_summary_

    Args:
        item_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        return database_load(item_id)
    except ItemNotFoundError as e:
        print(f"Logging ItemNotFoundError in load data: {e}")
        raise
    except DatabaseError as e:
        print(f"Logging DatabaseError in load data: {e}")
        raise


def main():
    """_summary_
    """
    item_ids = [1, 0, -1]

    for item_id in item_ids:
        try:
            print(load_data_centralized(item_id))
        except Exception as e:
            print(f"Propagation handling: {e}")
            traceback.print_exc()
        print("==============================")


if __name__ == "__main__":
    main()
