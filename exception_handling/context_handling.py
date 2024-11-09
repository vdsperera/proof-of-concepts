"""
2. Catching and Wrapping with Context (Chained Exceptions)

What It Is:
    Catching an exception in a lower-level function, adding contextual information
    (like in raise ... from e), and re-raising it.

How It’s Done: 
    Use a try-except block, catch the original exception, then raise a
    new exception with raise NewException(...) from e. This way, both
    the original and the new exceptions are available in the traceback.

When to Use:
    When you need to add context for a specific part of the code, like
    including details about a failed operation or adding a custom error
    message while preserving the original cause.
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


def load_data_with_context(item_id):
    """_summary_

    Args:
        item_id (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    try:
        return database_load(item_id)
    except DatabaseError as e:
        raise ValueError(f"Failed to load data for ID {item_id} due to a database error") from e
    except ItemNotFoundError as e:
        raise ValueError(f"Failed to load data for ID {item_id} because the item was not found") from e


def main():
    """_summary_
    """
    item_ids = [1, 0, -1]

    for item_id in item_ids:
        try:
            print(load_data_with_context(item_id))
        except Exception as e:
            print(f"Context handling: {e}")
            traceback.print_exc()
        print("==============================")


if __name__ == "__main__":
    main()
