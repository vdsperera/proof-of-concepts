"""
1. Exception Propagation

What It Is: 
    Letting an exception bubble up through layers of the application
    until it reaches a level where it’s handled (often in a top-level handler).

How It’s Done:
    Simply don’t catch the exception at lower levels. Python will automatically
    propagate it to the calling function until it reaches a handler or stops the
    program.

When to Use:
    When you want higher-level functions to handle the exception, or when lower-level
    functions aren’t in a position to handle the issue effectively.
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


def load_data_propagation(item_id):
    """_summary_

    Args:
        item_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    return database_load(item_id)


def main():
    """_summary_
    """
    item_ids = [1, 0, -1]

    for item_id in item_ids:
        try:
            print(load_data_propagation(item_id))
        except Exception as e:
            print(f"Propagation handling: {e}")
            traceback.print_exc()
        print("==============================")


if __name__ == "__main__":
    main()
